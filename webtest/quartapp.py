import json
from typing import List
from quart import Quart, request
from quart_cors import cors
from webtest.api import TelegramClient

def create_webapp(tgclients: List[TelegramClient]):
	app = Quart(__name__)
	# allow requests from the nextjs frontend dev server
	app = cors(app, allow_origin="http://localhost:3000")

	@app.route("/clients")
	async def clients():
		oldhash = request.args.get("hash")
		def makeblob(user: TelegramClient):
			return {
				"name": None,
				"username": None,
				"phone": user.auth.phone,
				"status": {
					"stage": user.auth.status.name,
					"inputRequired": user.auth.status.requiresInput,
				}
			}

		items = [makeblob(x) for x in tgclients]
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

			matching_client = next((client for client in tgclients if client.auth.phone == phone), None)

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

	return app