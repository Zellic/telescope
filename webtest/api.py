import asyncio
import random
import json
from typing import Callable, Any, Dict, List

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

class APIAuth:
	def __init__(self, phone):
		self.phone = phone
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

	def authorizationStateWaitTdlibParameters(self):
		self.status = WaitingOnServer()

	def authorizationStateReady(self):
		self.status = AuthorizationSuccess()

	def authorizationStateFailed(self):
		self.status = AuthorizationFailed()

	def authorizationStateWaitEmailAddress(self):
		self.status = EmailRequired()

		def wait(value):
			self._notify_event(InputReceived("email", value))

		self.status.waitForValue(wait)

	def authorizationStateWaitPassword(self):
		self.status = PasswordRequired()

		def wait(value):
			self._notify_event(InputReceived("password", value))

		self.status.waitForValue(wait)

	def authorizationStateWaitEmailCode(self):
		self.status = EmailCodeRequired()

		def wait(value):
			self._notify_event(InputReceived("email_code", value))

		self.status.waitForValue(wait)

	def authorizationStateWaitCode(self):
		self.status = AuthCodeRequired()

		def wait(value):
			self._notify_event(InputReceived("auth_code", value))

		self.status.waitForValue(wait)

async def fungleTheThingy(auth: APIAuth):
	auth.authorizationStateWaitPassword()
	await auth.status

	await asyncio.sleep(random.randint(15,20))

	auth.authorizationStateWaitCode()
	await auth.status

	await asyncio.sleep(random.randint(3, 5))

	auth.authorizationStateReady()

class TelegramClient:
	def __init__(self, auth: APIAuth):
		self.auth = auth
		self.client_id = random.randint(1,1000)
