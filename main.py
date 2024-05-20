import asyncio

from telegram.auth.production import ProductionWithPrompt
from telegram.client import TelegramClient
from telegram.auth.testaccount import TestAccount
from telegram.manager import TelegramClientManager


async def main():
	print("main")
	manager = TelegramClientManager()
	# manager.add_client(TelegramClient(TestAccount()))
	manager.add_client(TelegramClient(ProductionWithPrompt("16466565645")))
	# client.sendAwaitingReply({'@type': 'getOption', 'name': 'version', '@extra': 1.01234})

	# ugh
	# noinspection PyProtectedMember
	await asyncio.gather(*[x._task for x in manager.clients])

if __name__ == "__main__":
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	loop.run_until_complete(main())
	loop.close()