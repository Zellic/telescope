import asyncio
from webtest.api import TelegramClient, APIAuth, fungleTheThingy
from webtest.quartapp import create_webapp

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