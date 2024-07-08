import asyncio

from database.core import Database
from telegram.auth.api import APIAuth
from telegram.auth.schemes.live import TelegramProduction
from telegram.auth.schemes.staging import TelegramStaging
from telegram.client import TelegramClient
from telegram.manager import TelegramClientManager
from telegram.webapp import create_webapp
from tgmodules.savecontacts import SaveContacts
from tgmodules.userinfo import UserInfo


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

def clientFor(phonenumber, db, api_id, api_hash):
	scheme = TelegramProduction(api_id, api_hash, "accounts/" + phonenumber, True)
	return TelegramClient(APIAuth(phonenumber, scheme), [UserInfo(), SaveContacts(db, phonenumber)])

def testClientFor(phonenumber, db, api_id, api_hash):
	scheme = TelegramStaging(phonenumber, api_id, api_hash)
	return TelegramClient(APIAuth(phonenumber, scheme), [UserInfo()]) #, [SaveContacts(db, phonenumber)])

async def main():
	config = read_env_file(".env")
	db = Database(config['DB_DSN'])
	api = (config['API_ID'], config['API_HASH'])

	manager = TelegramClientManager()

	clients = [
		testClientFor(TelegramStaging.generate_phone(), db, *api),
		# clientFor("16466565645", db, *api),
		# clientFor("19295495669", db, *api),
		# clientFor("14052173620", db, *api),
	]

	for x in clients:
		manager.add_client(x)

	app = create_webapp([x for x in clients])

	# TODO: Python's async doesn't make this convenient. instead we probably need every client to be a
	# task while the run_until_complete loop simply rechecks whether len(manager.clients) > 0 every N
	# seconds with asyncio.sleep
	# noinspection PyProtectedMember
	await asyncio.gather(manager.start(), app.run_task("localhost", 8888))

if __name__ == "__main__":
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	loop.run_until_complete(main())
	loop.close()