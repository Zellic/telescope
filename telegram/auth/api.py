import json
from typing import Callable, List

from telegram.auth.base import AuthenticationProvider, APIAuthState, AuthenticationScheme
from telegram.client import TelegramClient

"""
This is the default state when the server hasn't asked us for anything yet.
"""
class WaitingOnServer(APIAuthState):
	name = "WaitingOnServer"
	requiresInput = False

class PasswordRequired(APIAuthState):
	name = "PasswordRequired"
	requiresInput = True

class AuthCodeRequired(APIAuthState):
	name = "AuthCodeRequired"
	requiresInput = True

class RegistrationRequired(APIAuthState):
	name = "RegistrationRequired"
	requiresInput = False

class PhoneNumberRequired(APIAuthState):
	name = "PhoneNumberRequired"
	requiresInput = False

class EmailRequired(APIAuthState):
	name = "EmailRequired"
	requiresInput = True

class EmailCodeRequired(APIAuthState):
	name = "EmailCodeRequired"
	requiresInput = True

class AuthorizationSuccess(APIAuthState):
	name = "AuthorizationSuccess"
	requiresInput = False

class AuthorizationFailed(APIAuthState):
	name = "AuthorizationFailed"
	requiresInput = False

class APIEvent:
	def to_json(self) -> str:
		return json.dumps(self.__dict__)

class NewAuthenticationStage(APIEvent):
	def __init__(self, stage: str):
		self.type = "NewAuthenticationState"
		self.state = stage

class InputReceived(APIEvent):
	def __init__(self, stage: str, value: str):
		self.type = "InputReceived"
		self.input_type = stage
		self.value = value

class APIAuth(AuthenticationProvider):
	def __init__(self, phone: str, scheme: AuthenticationScheme):
		self.phone = phone
		self.scheme = scheme
		self._status: APIAuthState = WaitingOnServer()
		self._event_callbacks: List[Callable[[APIEvent], None]] = []

	@property
	def status(self):
		return self._status

	@status.setter
	def status(self, value):
		self._status = value
		self._notify_event(NewAuthenticationStage(type(value).__name__))

	def add_event_callback(self, callback: Callable[[APIEvent], None]):
		self._event_callbacks.append(callback)

	def _notify_event(self, event: APIEvent):
		for callback in self._event_callbacks:
			callback(event)

	def authorizationStateWaitTdlibParameters(self, client: TelegramClient):
		self.scheme.authorizationStateWaitTdlibParameters(client)
		self.status = WaitingOnServer()

	def authorizationStateReady(self, client: TelegramClient):
		self.scheme.authorizationStateReady(client)
		self.status = AuthorizationSuccess()

	def authorizationStateClosed(self, client: TelegramClient):
		self.authorizationStateClosed(client)
		self.status = AuthorizationFailed()

	def authorizationStateWaitPhoneNumber(self, client: TelegramClient):
		self.scheme.authorizationStateWaitPhoneNumber(client, self.phone)
		self.status = PhoneNumberRequired()

	def authorizationStateWaitEmailAddress(self, client: TelegramClient):
		self.status = EmailRequired()

		def wait(value):
			self.scheme.authorizationStateWaitEmailAddress(client, value)
			self._notify_event(InputReceived(self.status.name, value))

		self.status.waitForValue(wait)

	def authorizationStateWaitPassword(self, client: TelegramClient):
		self.status = PasswordRequired()

		def wait(value):
			self.scheme.authorizationStateWaitPassword(client, value)
			self._notify_event(InputReceived(self.status.name, value))

		self.status.waitForValue(wait)

	def authorizationStateWaitEmailCode(self, client: TelegramClient):
		self.status = EmailCodeRequired()

		def wait(value):
			self.scheme.authorizationStateWaitEmailCode(client, value)
			self._notify_event(InputReceived(self.status.name, value))

		self.status.waitForValue(wait)

	def authorizationStateWaitCode(self, client: TelegramClient):
		self.status = AuthCodeRequired()

		def wait(value):
			self.scheme.authorizationStateWaitCode(client, value)
			self._notify_event(InputReceived(self.status.name, value))

		self.status.waitForValue(wait)

	# only implemented for staging, not used in production
	def authorizationStateWaitRegistration(self, client: 'TelegramClient'):
		self.status = RegistrationRequired()
		self.scheme.authorizationStateWaitRegistration(client, None)