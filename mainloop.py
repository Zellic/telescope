import asyncio
import os
import signal
import sys
from enum import Enum
from typing import Callable, Optional, Coroutine, Any

from quart import Quart

from database.accounts import AccountManager
from database.core import Database
from telegram.auth.base import StaticSecrets
from telegram.client import TelegramClient
from telegram.manager import TelegramClientManager
from telegram.util import Environment
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
	def __init__(self, environment: Environment):
		self.environment = environment
		self.config = dict(os.environ)

		# noinspection PyBroadException
		try:
			extra = read_env_file(".env")
			self.config.update(extra)
		except:
			pass

		if(len(self.config.get('TWO_FACTOR_ENCRYPTION_KEY', '')) != 32):
			raise Exception("Must set TWO_FACTOR_ENCRYPTION_KEY within environment file or environment variables.")

		self.db = Database(self.config['DB_DSN'])
		self.accounts = AccountManager(self.db, self.config['TWO_FACTOR_ENCRYPTION_KEY'])
		self.API_ID = self.config['API_ID']
		self.API_HASH = self.config['API_HASH']

		self.manager = TelegramClientManager()
		self._app: Optional[Quart] = None
		self._shutting_down = False
		self._idiot_quart_task = None

		self._did_init = False

	async def init(self):
		if(self._did_init):
			raise Exception("Cannot initialize twice.")

		self._did_init = True

		await self.accounts.init()

	def _check_init(self):
		if(not self._did_init):
			raise Exception("Not initialized...")

	async def addClient(self, client: TelegramClient):
		self._check_init()

		await self.manager.add_client(client)

	async def run(self, clientGenerator: Callable[[str], TelegramClient]):
		self._check_init()

		self._app = create_webapp(self.manager, self.accounts, clientGenerator, self.environment)
		host = "localhost" if self.config.get("DEBUG", "false").lower() == "true" else "0.0.0.0"

		self._idiot_quart_task = self._app.run_task(host, 8888)
		# we can't pass this to gather or it will eat control+c events for some reason...
		# it's okay because the manager runs forever, and we shut the manager down AFTER we shut the webapp down
		#
		# we awake .start() because we need the resulting task returned from it, not the async coroutine from the
		# async method...
		await asyncio.gather(await self.manager.start(), self._idiot_quart_task)

	async def shutdown(self):
		self._check_init()

		if(self._shutting_down):
			return

		self._shutting_down = True

		print("Shutting down...")

		if(self._app is not None):
			await self._app.shutdown()
			print("Webapp stopped")

		if(self.manager.is_started()):
			async for client in self.manager.stop_and_yield():
				print(f"Stopped client: {client.auth.phone}")

		await self.db.close_all()

		# apparently quart is just never going to shutdown properly
		# this library sucks
		sys.exit(0)

	def mainLoop(self, runOnStart: Callable[[], Coroutine[Any, Any, None]], clientGenerator: Callable[[str, Optional[str], Optional[StaticSecrets]], TelegramClient]):
		# make aiopg work on windows
		if sys.version_info >= (3, 8) and sys.platform.lower().startswith("win"):
			asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)
		shut_us_down = None

		def graceful_shutdown(*args):
			nonlocal shut_us_down
			if(self._shutting_down):
				return

			shut_us_down = asyncio.create_task(self.shutdown())

		# we do this because the Quart app sets its own close signal handlers that block ours (???)
		# so we take them back after the app's initialization is done
		# there is no race condition here as the app initialization happens instantly
		# we just need to make sure this happens after self.run(...) does
		async def hijack_close_signal():
			await asyncio.sleep(0.1)
			try:
				for sig in (signal.SIGINT, signal.SIGTERM):
					loop.add_signal_handler(sig, graceful_shutdown)
			# doesn't work on windows
			# can't use signal.signal because the handlers will be permanently blocked by the asyncio event loop
			# and we are allergic to threads
			except NotImplementedError:
				pass

		async def startup():
			await self.init()
			await runOnStart()
			await asyncio.gather(self.run(clientGenerator), hijack_close_signal())

		loop.run_until_complete(startup())
		if(shut_us_down is not None):
			loop.run_until_complete(shut_us_down)
		loop.close()