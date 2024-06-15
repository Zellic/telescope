import asyncio
from typing import List
from quart import Quart

from webtest.api import TelegramClient, APIAuth, fungleTheThingy


def create_webapp(clients: List[TelegramClient]):
	app = Quart(__name__)

	def status(x: TelegramClient):
		status = "unknown"
		if(isinstance(x.auth, APIAuth)):
			status = type(x.auth.status).__name__ + " (waiting on input: " + str(x.auth.status.requiresInput) + ")"

		return x.auth.phone + ": " + status

	@app.route("/")
	async def index():
		# TODO: escape this text as HTML entities
		return "<br />".join([status(x) for x in clients])

	return app

def clientFor(phone):
	return TelegramClient(APIAuth(phone=phone))

async def main():
	clients = [
		clientFor("16466565645"),
		clientFor("19295495669"),
		clientFor("14052173620"),
	]

	async def cringe():
		await asyncio.sleep(5)
		clients[0].auth.status.provideValue("we give the value")

	app = create_webapp(clients)

	await asyncio.gather(app.run_task("localhost", 8888), cringe(), *[fungleTheThingy(x.auth) for x in clients])

if __name__ == "__main__":
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	loop.run_until_complete(main())
	loop.close()