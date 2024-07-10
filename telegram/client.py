import asyncio
from typing import List

from telegram.auth.base import AuthenticationProvider
from telegram.tdlib import TDLib

class TelegramClient:
	def __init__(self, auth: AuthenticationProvider, modules: List[any]):
		# noinspection PyTypeChecker
		self._tdlib: TDLib = None
		self.auth = auth
		self.client_id = None

		self._modules = modules or []

		self._extra_counter = 0
		self._pending_responses = {}
		self._started = False

	def send(self, query):
		self._tdlib.send(self.client_id, query)

	"""
	send a tdlib query, awaiting a reply
	
	if used with a query type that does not cause a response this will await forever
	"""
	async def sendAwaitingReply(self, query):
		self._extra_counter += 1
		extra = self._extra_counter

		query['@extra'] = extra
		future = asyncio.get_event_loop().create_future()

		self._pending_responses[extra] = future

		self.send(query)

		return await future

	def _event_received(self, event):
		extra = event.get('@extra')
		if extra is not None:
			future = self._pending_responses.pop(extra, None)

			if future is not None:
				future.set_result(event)
				# a future handled this
				return

		if event['@type'] == 'updateAuthorizationState':
			auth_state = event['authorization_state']

			if auth_state['@type'] == 'authorizationStateClosed':
				# TODO: do something about this
				print("Authorization failed for: " + self.auth.phone)
				self.auth.authorizationStateFailed(self)
				return
			elif auth_state['@type'] == 'authorizationStateReady':
				print("Authorization successful for: " + self.auth.phone)
				self.auth.authorizationStateReady(self)
			else:
				method = getattr(self.auth, auth_state['@type'], None)

				if method is None:
					print(f"Unimplemented authorization state: {self.auth.phone} {auth_state['@type']}")
					raise NotImplementedError()

				method(self)
				return

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

		self.client_id = self._tdlib.create_client_id()
		self.send({'@type': 'getOption', 'name': 'version', '@extra': 1.01234})

	def stop(self):
		if (not self.is_started()):
			raise Exception("Hasn't been started yet")

		for module in self._modules:
			func = getattr(module, "onClientExit", None)

			if (func is not None):
				func()