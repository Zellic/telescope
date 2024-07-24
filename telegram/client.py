import asyncio
import sys
from typing import List

from telegram.auth.base import AuthenticationProvider
from telegram.tdlib import TDLib

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

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

		self._stop_future = None

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

		if event['@type'] == 'error':
			eprint(f"[!!! - {self.auth.phone}] an error occurred: {repr(event)}")

			# circular import lol
			from telegram.auth.api import ErrorOccurred
			if('code' in event):
				self.auth.status = ErrorOccurred(f"[{event['code']}] {event['message']}")
			else:
				self.auth.status = ErrorOccurred(f"{event['message']}")

			return
		elif event['@type'] == 'updateAuthorizationState':
			auth_state = event['authorization_state']

			if auth_state['@type'] == 'authorizationStateClosed':
				# TODO: this can be three different things and we can't distinguish via this message alone
				# - connection lost (could be our end, could be remote end)
				# - authorization failed (server closed connection on us, an explanation would've been sent in response to an earlier message)
				# - we disconnected (self._stop_future would be set)
				self.auth.authorizationStateClosed(self)

				if self._stop_future and not self._stop_future.done():
					self._stop_future.set_result(None)

				for module in self._modules:
					func = getattr(module, "onClientExit", None)

					if (func is not None):
						func()

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

		self._started = True

		self.client_id = self._tdlib.create_client_id()
		self.send({'@type': 'getOption', 'name': 'version', '@extra': 1.01234})

	async def stop(self):
		if (not self.is_started()):
			print("Client wasn't started yet.")
			return

		if(self._stop_future):
			if(self._stop_future.done()):
				print("Already stopped client, but received stop again???")
				return
			else:
				print("Client is already stopping, but received stop again")
				return

		self._stop_future = asyncio.Future()
		self.send({'@type': 'close'})

		await self._stop_future