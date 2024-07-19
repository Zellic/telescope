import asyncio
import os

from database.accounts import AccountManager
from database.core import Database
from telegram.auth.api import APIAuth
from telegram.auth.schemes.live import TelegramProduction
from telegram.auth.schemes.staging import TelegramStaging
from telegram.client import TelegramClient
from telegram.manager import TelegramClientManager
from telegram.tgmodules.savecontacts import SaveContacts
from telegram.webapp import create_webapp
from telegram.tgmodules.getcode import GetAuthCode
from telegram.tgmodules.userinfo import UserInfo

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
	return TelegramClient(APIAuth(phonenumber, scheme), [UserInfo(), SaveContacts(db, phonenumber), GetAuthCode()])

def testClientFor(phonenumber, db, api_id, api_hash):
	scheme = TelegramStaging(phonenumber, api_id, api_hash)
	return TelegramClient(APIAuth(phonenumber, scheme), [UserInfo()]) #, [SaveContacts(db, phonenumber)])

async def main():
	config = dict(os.environ)
	try:
		extra = read_env_file(".env")
		config.update(extra)
	except:
		pass
	db = Database(config['DB_DSN'])
	accounts = AccountManager(db)
	api = (config['API_ID'], config['API_HASH'])

	manager = TelegramClientManager()

	clients = [
		# testClientFor(TelegramStaging.generate_phone(), db, *api),
		# clientFor("16466565645", db, *api),
		# clientFor("19295495669", db, *api),
		# clientFor("14052173620", db, *api),
	]

	for account in accounts.getAccounts():
		clients.append(clientFor(account.phone_number, db, *api))

	for x in clients:
		manager.add_client(x)

	def clientForClosure(phonenumber):
		return clientFor(phonenumber, db, *api)

	app = create_webapp(manager, accounts, clientForClosure)

	# TODO: Python's async doesn't make this convenient. instead we probably need every client to be a
	# task while the run_until_complete loop simply rechecks whether len(manager.clients) > 0 every N
	# seconds with asyncio.sleep

	host = "localhost" if config.get("DEBUG", "false").lower() == "true" else "0.0.0.0"

	# async def lol():
	# 	await asyncio.sleep(5)
	# 	await next(x for x in clients[0]._modules if isinstance(x, GetAuthCode)).getAuthCode(clients[0])

	# noinspection PyProtectedMember
	await asyncio.gather(manager.start(), app.run_task(host, 8888))

if __name__ == "__main__":
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	loop.run_until_complete(main())
	loop.close()