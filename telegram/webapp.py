import json
import os
import re
from typing import List
from quart import request, Quart, send_from_directory, abort
from quart_cors import cors
from werkzeug.security import safe_join

from database.accounts import AccountManager
from telegram.client import TelegramClient
from telegram.manager import TelegramClientManager
from tgmodules.userinfo import UserInfo

ALLOWED_EXTENSIONS = {'html', 'js', 'css', 'png', 'jpg', 'gif', 'ico', 'svg'}
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_webapp(manager: TelegramClientManager, accounts: AccountManager, clientFor: any):
	app = Quart(__name__)
	# allow requests from the nextjs frontend dev server
	app = cors(app, allow_origin="http://localhost:3000")
	frontend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", 'telescope-webui-dist')

	@app.route("/clients")
	async def clients():
		oldhash = request.args.get("hash")
		def makeblob(user: TelegramClient):
			info_module = next((x for x in user._modules if isinstance(x, UserInfo)), None)
			info = info_module.info

			return {
				"name": None if info is None else info.first_name + " " + info.last_name,
				"username": None if info is None else info.username,
				"phone": user.auth.phone,
				"status": {
					"stage": user.auth.status.name,
					"inputRequired": user.auth.status.requiresInput,
				}
			}

		items = [makeblob(x) for x in manager.clients]
		ret = {
			'hash': str(hash(json.dumps(items))),
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
				return json.dumps({"error": "Invalid payload structure. 'phone_number' is required."}), 400

			phone_number = payload['phone_number']
			email = payload.get('email', None)
			comment = payload.get('comment', None)

			if not re.match(r'^\d{11}$', phone_number):
				return json.dumps({"error": "Phone number must be exactly 11 digits"}), 400

			if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
				return json.dumps({"error": "Invalid email format"}), 400

			if comment and (len(comment) < 1 or len(comment) > 300):
				return json.dumps({"error": "Comment must be between 1 and 300 characters"}), 400

			result = accounts.add_account(phone_number, email, comment)

			if result.success:
				manager.add_client(clientFor(phone_number))
				return json.dumps({"message": "Account added successfully"}), 201
			else:
				return json.dumps({"error": result.error_message}), 400
		except Exception as e:
			return json.dumps({"error": f"Unexpected error: {str(e)}"}), 500

	@app.route('/<path:filename>')
	async def serve_static(filename):
		if not allowed_file(filename):
			abort(404)
		safe_path = safe_join(frontend_path, filename)
		# path traversal
		if safe_path is None:
			abort(404)
		if os.path.isfile(safe_path):
			return await send_from_directory(frontend_path, filename)
		abort(404)

	@app.route('/', defaults={'path': ''})
	@app.route('/<path:path>')
	async def serve_index(path):
		return await send_from_directory(frontend_path, 'index.html')

	return app