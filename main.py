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

def clientFor(phonenumber, db):
	return TelegramClient(ProductionWithPrompt(phonenumber), [SaveContacts(db, phonenumber)])

# TODO: ignore group chats
async def main():
	config = read_env_file(".env")
	db = Database(config['DB_DSN'])

	manager = TelegramClientManager()
	# manager.add_client(TelegramClient(TestAccount(), [SaveContacts(db)]))
	# manager.add_client(clientFor("16466565645", db))
	# manager.add_client(clientFor("19295495669", db))
	manager.add_client(clientFor("14052173620", db))

	# TODO: Python's async doesn't make this convenient. instead we probably need every client to be a
	# task while the run_until_complete loop simply rechecks whether len(manager.clients) > 0 every N
	# seconds with asyncio.sleep
	# noinspection PyProtectedMember
	await asyncio.gather(manager.start())

if __name__ == "__main__":
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	loop.run_until_complete(main())
	loop.close()