import asyncio

from database.core import Database
from telegram.auth.production import ProductionWithPrompt
from telegram.client import TelegramClient
from telegram.auth.testaccount import TestAccount
from telegram.manager import TelegramClientManager
from tgmodules.savecontacts import SaveContacts

# dotenv wouldn't install...
def read_env_file(file_path):
	env_dict = {}

	with open(file_path, 'r') as file:
		for line in file:
			line = line.strip()
			if not line:
				continue

			key, value = line.split('=', 1)

			key = key.strip()
			value = value.strip()

			if value.startswith('"') and value.endswith('"'):
				value = value[1:-1]

			env_dict[key] = value

	return env_dict

# TODO: ignore group chats
async def main():
	config = read_env_file(".env")
	db = Database(config['DB_DSN'])

	manager = TelegramClientManager()
	# manager.add_client(TelegramClient(TestAccount(), [SaveContacts()]))
	manager.add_client(TelegramClient(ProductionWithPrompt("16466565645"), [SaveContacts()]))
	# client.sendAwaitingReply({'@type': 'getOption', 'name': 'version', '@extra': 1.01234})

	# TODO: Python's async doesn't make this convenient. instead we probably need every client to be a
	# task while the run_until_complete loop simply rechecks whether len(manager.clients) > 0 every N
	# seconds with asyncio.sleep
	# noinspection PyProtectedMember
	await asyncio.gather(*[x._task for x in manager.clients])

if __name__ == "__main__":
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	loop.run_until_complete(main())
	loop.close()