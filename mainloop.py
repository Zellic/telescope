import asyncio
import os
import signal
import sys
from asyncio import Task
from typing import Callable, List, Optional

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

		self._tasks: Optional[List[Task]] = None

	def addClient(self, client: TelegramClient):
		self.manager.add_client(client)

	async def run(self, clientGenerator: Callable[[str], TelegramClient]):
		app = create_webapp(self.manager, self.accounts, clientGenerator)
		host = "localhost" if self.config.get("DEBUG", "false").lower() == "true" else "0.0.0.0"

		self._tasks = [
			app.run_task(host, 8888),
		]

		await asyncio.gather(self.manager.start(), *self._tasks)

	async def shutdown(self):
		print("Shutting down...")

		for task in self._tasks:
			try:
				task.cancel()
			except asyncio.CancelledError:
				pass

		async for client in self.manager.stop_and_yield():
			print(f"Stopped client: {client.auth.phone}")

	def mainLoop(self, clientGenerator: Callable[[str], TelegramClient]):
		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)

		def graceful_shutdown(*args):
			def _stop():
				# we assume the running loop couldn't have changed (?)
				loop.stop()
				sys.exit(0)

			asyncio.create_task(self.shutdown()).add_done_callback(lambda x: _stop())

		signal.signal(signal.SIGINT, graceful_shutdown)
		signal.signal(signal.SIGTERM, graceful_shutdown)

		loop.run_until_complete(self.run(clientGenerator))
		loop.close()