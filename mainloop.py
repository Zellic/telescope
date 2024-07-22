import asyncio
import os
from typing import Callable

from database.accounts import AccountManager
from database.core import Database
from telegram.client import TelegramClient
from telegram.manager import TelegramClientManager
from telegram.webapp import create_webapp

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

class MainLoop:
	def __init__(self):
		self.config = dict(os.environ)

		# noinspection PyBroadException
		try:
			extra = read_env_file(".env")
			self.config.update(extra)
		except:
			pass

		self.db = Database(self.config['DB_DSN'])
		self.accounts = AccountManager(db)
		self.API_ID = self.config['API_ID']
		self.API_HASH = self.config['API_HASH']

		self.manager = TelegramClientManager()

	def addClient(self, client: TelegramClient):
		self.manager.add_client(client)

	async def run(self, clientGenerator: Callable[[str], TelegramClient]):
		app = create_webapp(self.manager, self.accounts, clientGenerator)
		host = "localhost" if self.config.get("DEBUG", "false").lower() == "true" else "0.0.0.0"

		# noinspection PyProtectedMember
		await asyncio.gather(self.manager.start(), app.run_task(host, 8888))

	def mainLoop(self):
		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)
		loop.run_until_complete(self.run())
		loop.close()