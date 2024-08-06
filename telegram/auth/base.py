import asyncio
from dataclasses import dataclass
from typing import Optional


class APIAuthState:
	name: str
	requiresInput: bool

	def __init__(self):
		self.listeners = []

	def waitForValue(self, callback):
		self.listeners.append(callback)

	def provideValue(self, value):
		for func in self.listeners:
			func(value)
		self.listeners = []
		self.requiresInput = False

	def __await__(self):
		self.future = asyncio.Future()
		self.waitForValue(lambda value: self.future.set_result(value))
		return self.future.__await__()

@dataclass
class StaticSecrets:
	two_factor_password: Optional[str]

class AuthenticationScheme:
	secrets: Optional[StaticSecrets]

	def authorizationStateClosing(self, client: 'TelegramClient'):
		pass

	def authorizationStateClosed(self, client: 'TelegramClient'):
		pass

	def authorizationStateReady(self, client: 'TelegramClient'):
		pass

	def authorizationStateWaitTdlibParameters(self, client: 'TelegramClient'):
		raise NotImplementedError()

	def authorizationStateWaitPhoneNumber(self, client: 'TelegramClient', value: any):
		raise NotImplementedError()

	def authorizationStateWaitEmailAddress(self, client: 'TelegramClient', value: any):
		raise NotImplementedError()

	def authorizationStateWaitEmailCode(self, client: 'TelegramClient', value: any):
		raise NotImplementedError()

	def authorizationStateWaitCode(self, client: 'TelegramClient', value: any):
		raise NotImplementedError()

	def authorizationStateWaitRegistration(self, client: 'TelegramClient', value: any):
		raise NotImplementedError()

	def authorizationStateWaitPassword(self, client: 'TelegramClient', value: any):
		raise NotImplementedError()

# this is a wrapper used by stdin and web input to provide secrets during auth flow
class AuthenticationProvider:
	phone: str
	status: APIAuthState
	scheme: AuthenticationScheme

	def authorizationStateClosing(self, client: 'TelegramClient'):
		pass

	def authorizationStateClosed(self, client: 'TelegramClient'):
		pass

	def authorizationStateReady(self, client: 'TelegramClient'):
		pass

	def authorizationStateWaitTdlibParameters(self, client: 'TelegramClient'):
		raise NotImplementedError()

	def authorizationStateWaitPhoneNumber(self, client: 'TelegramClient'):
		raise NotImplementedError()

	def authorizationStateWaitEmailAddress(self, client: 'TelegramClient'):
		raise NotImplementedError()

	def authorizationStateWaitEmailCode(self, client: 'TelegramClient'):
		raise NotImplementedError()

	def authorizationStateWaitCode(self, client: 'TelegramClient'):
		raise NotImplementedError()

	def authorizationStateWaitRegistration(self, client: 'TelegramClient'):
		raise NotImplementedError()

	def authorizationStateWaitPassword(self, client: 'TelegramClient'):
		raise NotImplementedError()
