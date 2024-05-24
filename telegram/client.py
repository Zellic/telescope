import asyncio
from typing import List

from telegram.auth.base import AuthenticationScheme
from telegram.tdlib import TDLib

class TelegramClient:
	def __init__(self, auth: AuthenticationScheme, modules: List[any]):
		self.tdlib = TDLib()
		self.auth = auth
		self.client_id = self.tdlib.create_client_id()

		self._modules = modules or []

		self._extra_counter = 0
		self._pending_responses = {}
		self._lock = asyncio.Lock()
		self._stop_event = asyncio.Event()
		self._task = None
		# errors
		self.tdlib.td_execute({'@type': 'setLogVerbosityLevel', 'new_verbosity_level': 1})
		self._started = False

	def send(self, query):
		self.tdlib.send(self.client_id, query)

	"""
	send a tdlib query, awaiting a reply
	
	if used with a query type that does not cause a response this will await forever
	"""
	async def sendAwaitingReply(self, query):
		async with self._lock:
			self._extra_counter += 1
			extra = self._extra_counter

		query['@extra'] = extra
		future = asyncio.get_event_loop().create_future()

		async with self._lock:
			self._pending_responses[extra] = future

		self.send(query)

		return await future

	async def _receive_loop(self):
		while not self._stop_event.is_set():
			event = await asyncio.to_thread(self.tdlib.receive)

			if event is None:
				continue

			extra = event.get('@extra')
			if extra is not None:
				async with self._lock:
					future = self._pending_responses.pop(extra, None)

				if future is not None:
					future.set_result(event)
					# loop because a future handled this
					continue

			if event['@type'] == 'updateAuthorizationState':
				auth_state = event['authorization_state']

				if auth_state['@type'] == 'authorizationStateClosed':
					print("Authorization failed.")
					break
				elif auth_state['@type'] == 'authorizationStateReady':
					print("Authorization successful.")
				else:
					method = getattr(self.auth, auth_state['@type'], None)

					if method is None:
						print(f"Unimplemented authorization state: {auth_state['@type']}")
						raise NotImplementedError()

					method(self)
					continue

			for module in self._modules:
				func = getattr(module, event['@type'], None)

				if(func is not None):
					# noinspection PyAsyncCall
					asyncio.create_task(func(self, event))

	def is_started(self):
		return self._started

	def start(self):
		if(self.is_started()):
			raise Exception("Already started")

		self._started = True
		self._task = asyncio.get_event_loop().create_task(self._receive_loop())
		self.send({'@type': 'getOption', 'name': 'version', '@extra': 1.01234})

	async def stop(self):
		if(not self.is_started()):
			raise Exception("Hasn't been started yet")

		for module in self._modules:
			func = getattr(module, "onClientExit", None)

			if(func is not None):
				func()

		self._stop_event.set()
		await self._task

	# async def on_message(self, event):
	# 	if event['@type'] == 'updateConnectionState':
	# 		if event['state']['@type'] == 'connectionStateReady':
	# 			# TODO: modules
	# 			wot = await self.sendAwaitingReply({'@type': 'getChats', 'limit': 100})