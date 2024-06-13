import random
from telegram.auth.base import AuthenticationScheme
from telegram.client import TelegramClient

class TestAccount(AuthenticationScheme):
	def __init__(self, api_id, api_hash):
		self.api_id = api_id
		self.api_hash = api_hash
		code = str(random.randint(0, 9))
		end = random.randint(0, 9999)
		self.end = f"{end:04d}"
		self.phone = f"99966{code}{self.end}"
		self.code = code * 5

	def authorizationStateWaitTdlibParameters(self, client: TelegramClient):
		client.send({
			'@type': 'setTdlibParameters',
			'database_directory': 'tdlib',
			'use_message_database': True,
			'use_secret_chats': False,
			'use_test_dc': True,
			'api_id': self.api_id,
			'api_hash': self.api_hash,
			'system_language_code': 'en',
			'device_model': 'Desktop',
			'application_version': '0.1'
		})

	def authorizationStateWaitPhoneNumber(self, client: TelegramClient):
		client.send({'@type': 'setAuthenticationPhoneNumber', 'phone_number': self.phone})

	def authorizationStateWaitEmailAddress(self, client: TelegramClient):
		# client.send({'@type': 'setAuthenticationEmailAddress', 'email_address': "nobody@gmail.com"})
		raise NotImplementedError()

	def authorizationStateWaitRegistration(self, client: TelegramClient):
		client.send({'@type': 'registerUser', 'first_name': "Herp", 'last_name': "Derp"})

	def authorizationStateWaitPassword(self, client: TelegramClient):
		client.send({'@type': 'checkAuthenticationPassword', 'password': "password"})