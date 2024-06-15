import asyncio
import random

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

class APIAuth:
	def __init__(self, phone):
		self.phone = phone
		self.status: APIAuthState = WaitingOnServer()

	def authorizationStateWaitTdlibParameters(self):
		self.status = WaitingOnServer()

	def authorizationStateReady(self):
		self.status = AuthorizationSuccess()

	def authorizationStateFailed(self):
		self.status = AuthorizationFailed()

	def authorizationStateWaitEmailAddress(self):
		self.status = EmailRequired()

		def wait(value):
			print(f"received email: {value}")

		self.status.waitForValue(wait)

	def authorizationStateWaitPassword(self):
		self.status = PasswordRequired()

		def wait(value):
			print(f"received password: {value}")

		self.status.waitForValue(wait)

	def authorizationStateWaitEmailCode(self):
		self.status = EmailCodeRequired()

		def wait(value):
			print(f"received email code: {value}")

		self.status.waitForValue(wait)

	def authorizationStateWaitCode(self):
		self.status = AuthCodeRequired()

		def wait(value):
			print(f"received auth code: {value}")

		self.status.waitForValue(wait)

async def fungleTheThingy(auth: APIAuth):
	auth.authorizationStateWaitPassword()
	await auth.status

	await asyncio.sleep(random.randint(1,3))

	auth.authorizationStateWaitCode()
	await auth.status

	await asyncio.sleep(random.randint(1, 3))

	auth.authorizationStateReady()

class TelegramClient:
	def __init__(self, auth: APIAuth):
		self.auth = auth
		self.client_id = random.randint(1,1000)
