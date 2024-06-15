from typing import List
from quart import Quart

from webtest.api import TelegramClient

def create_webapp(clients: List[TelegramClient]):
	app = Quart(__name__)

	def status(x: TelegramClient):
		status_str = type(x.auth.status).__name__ + " (waiting on input: " + str(x.auth.status.requiresInput) + ")"
		return x.auth.phone + ": " + status_str

	@app.route("/")
	async def index():
		# TODO: escape this text as HTML entities
		return "<br />".join([status(x) for x in clients])

	@app.route("/clients")
	async def clients():
		return [
			{
				"phone": x.auth.phone,
				"status": {
					"name": x.auth.status.name,
					"inputRequired": x.auth.status.requiresInput,
				}
			} for x in clients
		]

	return app