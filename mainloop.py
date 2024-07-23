import asyncio
import os
import signal
import sys
from asyncio import Task
from typing import Callable, List, Optional

from quart import Quart

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
		self.accounts = AccountManager(self.db)
		self.API_ID = self.config['API_ID']
		self.API_HASH = self.config['API_HASH']

		self.manager = TelegramClientManager()
		self._app: Optional[Quart] = None

	def addClient(self, client: TelegramClient):
		self.manager.add_client(client)

	async def run(self, clientGenerator: Callable[[str], TelegramClient]):
		self._app = create_webapp(self.manager, self.accounts, clientGenerator)
		host = "localhost" if self.config.get("DEBUG", "false").lower() == "true" else "0.0.0.0"

		await asyncio.gather(self.manager.start(), self._app.run_task(host, 8888))

	async def shutdown(self):
		print("Shutting down...")

		if(self._app is not None):
			await self._app.shutdown()

		async for client in self.manager.stop_and_yield():
			print(f"Stopped client: {client.auth.phone}")

	def mainLoop(self, clientGenerator: Callable[[str], TelegramClient]):
		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)

		def graceful_shutdown(*args):
			def _stop():
				# we assume the running loop couldn't have changed (?)
				loop.stop()

			asyncio.create_task(self.shutdown()).add_done_callback(lambda x: _stop())

		try:
			for sig in (signal.SIGINT, signal.SIGTERM):
				loop.add_signal_handler(sig, graceful_shutdown)
		# doesn't work on windows
		# can't use signal.signal because the handlers will be permanently blocked by the asyncio event loop
		# and we are allergic to threads
		except NotImplementedError:
			pass

		loop.run_until_complete(self.run(clientGenerator))
		loop.close()