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
	"""
	Handles the core Telegram authentication protocol and API communication.
	
	This class is responsible for:
	- Managing Telegram API parameters (API ID, hash, database directory)
	- Sending authentication requests to Telegram's servers
	- Implementing the low-level authentication protocol
	
	It does NOT handle user input collection - it only knows how to communicate
	with Telegram once it receives the required values (phone numbers, codes, etc.).
	
	Examples: TelegramProduction, TelegramDevelopment
	"""

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

class AuthenticationProvider:
	"""
	Collects user input during authentication and delegates to an AuthenticationScheme.
	
	This class is responsible for:
	- Gathering user input (phone numbers, codes, passwords) through various methods
	- Managing authentication state and status
	- Providing different input interfaces (console, web API, etc.)
	- Delegating actual Telegram communication to an AuthenticationScheme
	
	It acts as a wrapper/adapter that handles user interaction while the scheme
	handles the actual Telegram protocol. This separation allows mixing different
	input methods with different Telegram configurations.
	
	Examples: APIAuth (web interface), ProductionWithPrompt (console input)
	"""

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
