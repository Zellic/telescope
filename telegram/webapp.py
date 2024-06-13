from typing import List
from quart import Quart

from telegram.auth.api import APIAuth

def create_webapp(clients: List[APIAuth]):
	app = Quart(__name__)

	@app.route("/")
	async def index():
		return "dfgdsfgsdfg"

	return app