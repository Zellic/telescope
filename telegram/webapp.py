from typing import List
from quart import Quart

from telegram.auth.api import APIAuth
from telegram.client import TelegramClient

def create_webapp(clients: List[TelegramClient]):
	app = Quart(__name__)

	def status(x: TelegramClient):
		status = "unknown"
		if(isinstance(x.auth, APIAuth)):
			status = type(x.auth.status).__name__ + " (waiting on input: " + str(x.auth.status.requiresInput) + ")"

		return x.auth.phone + ": " + status

	@app.route("/")
	async def index():
		wtf = [status(x) for x in clients]
		print("wtf: " + repr(wtf))
		return "<br />".join(wtf)

	return app