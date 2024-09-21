import asyncio
import json
import os
import re
import sys

from quart import request, Quart, send_from_directory, abort, Response
from quart_cors import cors

from database.accounts import AccountManager, Account
from telegram.auth.api import AuthorizationSuccess, ConnectionClosed, ClientNotStarted
from telegram.auth.base import StaticSecrets
from telegram.auth.schemes.staging import TelegramStaging
from telegram.client import TelegramClient
from telegram.manager import TelegramClientManager
from telegram.tgmodules.getcode import GetAuthCode
from telegram.tgmodules.userinfo import UserInfo
from telegram.util import Environment

ALLOWED_EXTENSIONS = {'html', 'js', 'css', 'png', 'jpg', 'gif', 'ico', 'svg'}
def is_allowed_file(path, root):
	try:
		real_path = os.path.realpath(path)
		real_root = os.path.realpath(root)

		common_prefix = os.path.commonpath([real_path, real_root])

		return common_prefix == real_root
	except ValueError:
		return False
	except OSError:
		return False

def create_webapp(manager: TelegramClientManager, accounts: AccountManager, clientFor: any, environment: Environment):
	execution_environment = environment
	app = Quart(__name__)
	# allow requests from the nextjs frontend dev server
	app = cors(app, allow_origin="http://localhost:3000")
	frontend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", 'telescope-webui-dist')
	lookup = {}

	async def _get_account(phone: str) -> Account:
		if (phone in lookup):
			account = lookup[phone]
		else:
			account = await accounts.get_account(phone)

		lookup[phone] = account
		return account

	@app.route("/clients")
	async def clients():
		oldhash = request.args.get("hash")
		async def makeblob(user: TelegramClient):
			info_module = next((x for x in user._modules if isinstance(x, UserInfo)), None)
			info = None if info_module is None else info_module.info

			code_module = next((x for x in user._modules if isinstance(x, GetAuthCode)), None)

			# TODO: should probably batch this...
			account = await _get_account(user.auth.phone)

			return {
				"name": None if info is None or info.first_name is None or info.last_name is None else info.first_name + " " + info.last_name,
				"username": None if info is None else info.username,
				"phone": user.auth.phone,
				"email": None if account is None else account.email,
				"comment": None if account is None else account.comment,
				"lastCode": None if code_module is None or code_module.code is None else {
					"value": int(code_module.code),
					"date": code_module.timestamp,
				},
				"two_factor_pass_is_set": False if account is None else account.two_factor_password is not None,
				"status": {
					"stage": user.auth.status.name,
					"inputRequired": user.auth.status.requiresInput,
					"error": user.auth.status.error if hasattr(user.auth.status, "error") else None,
				}
			}

		items = [await makeblob(x) for x in manager.clients]
		ret = {
			'hash': str(hash(json.dumps(items))),
			'environment': execution_environment.name,
			'items': items,
		}

		if(oldhash is not None and ret['hash'] == oldhash):
			return {'hash': ret['hash']}

		return ret

	@app.route("/submitvalue", methods=["POST"])
	async def submit():
		try:
			payload = json.loads(await request.get_data())

			if not all(key in payload for key in ['phone', 'stage', 'value']):
				return json.dumps({"error": "Invalid payload structure"}), 400

			phone = payload['phone']
			stage = payload['stage']
			value = payload['value']

			matching_client = next((client for client in manager.clients if client.auth.phone == phone), None)

			if not matching_client:
				return json.dumps({"error": f"No client found with phone number {phone}"}), 404

			if matching_client.auth.status.name != stage:
				return json.dumps(
					{"error": f"Client stage mismatch. Expected {matching_client.auth.status.name}, got {stage}"}), 400

			try:
				matching_client.auth.status.provideValue(value)
				return json.dumps({"message": "Value provided successfully"}), 200
			except Exception as e:
				return json.dumps({"error": f"Error providing value: {str(e)}"}), 500
		except Exception as e:
			return json.dumps({"error": f"Unexpected error: {str(e)}"}), 500

	@app.route("/addtgaccount", methods=["POST"])
	async def addtgaccount():
		try:
			payload = json.loads(await request.get_data())

			if not all(key in payload for key in ['phone_number']):
				print("failed to add account: phone number is required")
				return json.dumps({"error": "Invalid payload structure. 'phone_number' is required."}), 400

			phone_number = payload['phone_number']
			email = payload.get('email', None)
			comment = payload.get('comment', None)

			if not re.match(r'^\d{11}$', phone_number):
				print("failed to add account: phone number must be 11 digits")
				return json.dumps({"error": "Phone number must be exactly 11 digits"}), 400

			if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
				print("failed to add account: invalid email format")
				return json.dumps({"error": "Invalid email format"}), 400

			if comment and (len(comment) < 1 or len(comment) > 300):
				print("failed to add account: comment must be between 1 and 300 characters")
				return json.dumps({"error": "Comment must be between 1 and 300 characters"}), 400

			result = await accounts.add_account(phone_number, email, comment)

			if result.success:
				await manager.add_client(clientFor(phone_number))
				print(f"failed to add account: added account successfully ({phone_number})")
				return json.dumps({"message": "Account added successfully"}), 201
			else:
				print(f"failed to add account: {result.error_message}")
				return json.dumps({"error": result.error_message}), 400
		except Exception as e:
			print(f"failed to add account: unexpected error - {str(e)}")
			return json.dumps({"error": f"Unexpected error: {str(e)}"}), 500

	@app.route("/prometheus")
	async def prometheus():
		out = [
			'# HELP telescope_auth_status Authentication status for clients',
			'# TYPE telescope_auth_status gauge'
		]

		for user in manager.clients:
			if isinstance(user.auth.status, ConnectionClosed):
				out.append(
					f'telescope_auth_status{{phone="{user.auth.phone}",stage="{user.auth.status.name}",status="failed"}} 1')
			elif not isinstance(user.auth.status, AuthorizationSuccess):
				if user.auth.status.requiresInput:
					out.append(
						f'telescope_auth_status{{phone="{user.auth.phone}",stage="{user.auth.status.name}",status="input_required"}} 1')
				else:
					out.append(
						f'telescope_auth_status{{phone="{user.auth.phone}",stage="{user.auth.status.name}",status="waiting_on_server"}} 1')

		metrics_text = '\n'.join(out)
		return Response(metrics_text, mimetype="text/plain")

	@app.route("/tgdisconnect")
	async def tgdisconnect():
		phone = request.args.get("phone")
		client = next((x for x in manager.clients if x.auth.phone == phone), None)

		if(client is None):
			return json.dumps({"error": f"Couldn't find client with phone number: {phone}"}), 500

		if(not client.is_started()):
			return json.dumps({"error": f"Client was not started"}), 500

		if(client.is_stopped()):
			return json.dumps({"error": f"Client is already stopped"}), 500

		if(client.is_stopping()):
			return json.dumps({"error": f"Client is already stopping"}), 500

		async def shutdown_client():
			info_module = next((x for x in client._modules if isinstance(x, UserInfo)), None)
			info = None if info_module is None else info_module.info

			await client.stop()

			manager.clients.remove(client)
			client.auth.status = ClientNotStarted()
			await manager.add_client(client, start=False) #clientFor(phone, None if info is None else info.db_username(), _get_account(phone)), False)

		await asyncio.create_task(shutdown_client())
		return json.dumps({"message": "Client is now disconnecting"}), 200

	# noinspection PyProtectedMember
	@app.route("/tgconnect")
	async def tgconnect():
		phone = request.args.get("phone")
		client = next((x for x in manager.clients if x.auth.phone == phone), None)

		if(client is None):
			return json.dumps({"error": f"Couldn't find client with phone number: {phone}"}), 500

		if(client.is_started()):
			return json.dumps({"error": f"Client is already started"}), 500

		await client.start()
		return json.dumps({"message": "Client is now starting"}), 200

	@app.route("/deleteaccount")
	async def deleteaccount():
		phone = request.args.get("phone")
		client = next((x for x in manager.clients if x.auth.phone == phone), None)

		if(client is None):
			return json.dumps({"error": f"Couldn't find client with phone number: {phone}"}), 500

		async def shutdown_and_remove():
			if (client is not None and not client.is_stopped()):
				if (not client.is_stopping()):
					await client.stop()
				else:
					# noinspection PyProtectedMember
					await client._stop_future

			manager.clients.remove(client)
			result = await accounts.delete_account(phone)

			if(not result.success):
				sys.stderr.write(f"[!] Could not delete account {phone}: {result.error_code} / {result.error_message}\n")

		await asyncio.create_task(shutdown_and_remove())
		return json.dumps({"message": "Client is now disconnecting and will be removed"}), 200

	@app.route("/setpassword", methods=['POST'])
	async def setpassword():
		try:
			payload = json.loads(await request.get_data())
		except:
			return json.dumps({"error": f"Bad JSON payload"}), 500

		if not all(key in payload for key in ['password']):
			print("failed to set password: password is required")
			return json.dumps({"error": "Invalid payload structure. 'password' is required."}), 400

		phone = request.args.get("phone")
		client = next((x for x in manager.clients if x.auth.phone == phone), None)

		if(client is None):
			return json.dumps({"error": f"Couldn't find client with phone number: {phone}"}), 500

		res = await accounts.set_two_factor_password(phone, payload['password'])

		if(res.success):
			(await _get_account(phone)).two_factor_password = payload['password']

			if(client.auth.scheme.secrets is not None):
				client.auth.scheme.secrets.two_factor_password = payload['password']
			else:
				client.auth.scheme.secrets = StaticSecrets(two_factor_password=payload['password'])

			return json.dumps({"message": "Password set successfully."}), 200
		else:
			sys.stderr.write("[!] failed to set password on account due to DB error: " + res.error_message + "\n")
			return json.dumps({"error": "Failed to set password due to DB error, see stderr."}), 400

	@app.route('/environment')
	async def environment():
		return json.dumps({"environment": execution_environment.name})

	@app.route('/addtestaccount')
	async def addtestaccount():
		phone = TelegramStaging.generate_phone()
		email = ''
		comment = ''

		result = await accounts.add_account(phone, email, comment, True)

		if result.success:
			await manager.add_client(clientFor(phone))
			print(f"failed to add account: added account successfully ({phone})")
			return json.dumps({"message": "Account added successfully"}), 201
		else:
			print(f"failed to add account: {result.error_message}")
			return json.dumps({"error": result.error_message}), 400

	@app.route('/<path:asset_path>')
	async def serve_static(asset_path):
		path = os.path.join(frontend_path, asset_path)
		if not is_allowed_file(path, frontend_path):
			abort(404)
		if os.path.isfile(path):
			return await send_from_directory(frontend_path, asset_path)
		abort(404)

	@app.route('/', defaults={'path': ''})
	@app.route('/<path:path>')
	async def serve_index(path):
		return await send_from_directory(frontend_path, 'index.html')

	return app