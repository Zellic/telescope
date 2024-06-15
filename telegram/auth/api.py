from telegram.auth.base import AuthenticationScheme
from telegram.client import TelegramClient

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

class APIAuth(AuthenticationScheme):
	def __init__(self, phone, api_id, api_hash):
		self.phone = phone
		self.api_id = api_id
		self.api_hash = api_hash
		self.status = None

	def authorizationStateWaitTdlibParameters(self, client: TelegramClient):
		client.send({
			'@type': 'setTdlibParameters',
			'database_directory': 'accounts/' + self.phone,
			'use_message_database': True,
			'use_secret_chats': False,
			'api_id': self.api_id,
			'api_hash': self.api_hash,
			'system_language_code': 'en',
			'device_model': 'Desktop',
			'application_version': '0.1'
		})
		self.status = WaitingOnServer()

	def authorizationStateReady(self, client: TelegramClient):
		self.status = AuthorizationSuccess()

	def authorizationStateFailed(self, client: TelegramClient):
		self.status = AuthorizationFailed()

	def authorizationStateWaitPhoneNumber(self, client: TelegramClient):
		client.send({'@type': 'setAuthenticationPhoneNumber', 'phone_number': self.phone})

	def authorizationStateWaitEmailAddress(self, client: TelegramClient):
		self.status = EmailRequired()

		def wait(value):
			client.send({'@type': 'setAuthenticationEmailAddress', 'email_address': value})

		self.status.waitForValue(wait)

	def authorizationStateWaitPassword(self, client: TelegramClient):
		self.status = PasswordRequired()

		def wait(value):
			client.send({'@type': 'checkAuthenticationPassword', 'password': value})

		self.status.waitForValue(wait)

	def authorizationStateWaitEmailCode(self, client: 'TelegramClient'):
		self.status = EmailCodeRequired()

		def wait(value):
			client.send({'@type': 'checkAuthenticationEmailCode',
			             'code': {'@type': 'emailAddressAuthenticationCode', 'code': value}})

		self.status.waitForValue(wait)

	def authorizationStateWaitCode(self, client: 'TelegramClient'):
		self.status = AuthCodeRequired()

		def wait(value):
			client.send({'@type': 'checkAuthenticationCode', 'code': value})

		self.status.waitForValue(wait)