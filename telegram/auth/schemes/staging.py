import random
from telegram.auth.base import AuthenticationProvider, AuthenticationScheme
from telegram.client import TelegramClient

class TelegramStaging(AuthenticationScheme):
	@staticmethod
	def generate_phone():
		code = str(random.randint(1, 3))
		end = random.randint(1111, 9999)
		ends = f"{end:04d}"
		return f"99966{code}{ends}"

	def __init__(self, phone, api_id, api_hash, db_directory: str):
		self.api_id = api_id
		self.api_hash = api_hash
		self.db_directory = db_directory
		assert(phone[0:5] == '99966')
		assert(len(phone) == 10)
		self.phone = phone
		self.code = phone[5] * 5
		print("Phone: " + repr(self.phone) +  ", code: " + repr(self.code))

	def authorizationStateWaitTdlibParameters(self, client: TelegramClient):
		client.send({
			'@type': 'setTdlibParameters',
			'database_directory': self.db_directory,
			'use_message_database': False,
			'use_secret_chats': False,
			'use_test_dc': True,
			'api_id': self.api_id,
			'api_hash': self.api_hash,
			'system_language_code': 'en',
			'device_model': 'Desktop',
			'application_version': '0.1'
		})

	def authorizationStateWaitPhoneNumber(self, client: TelegramClient, value: any):
		client.send({'@type': 'setAuthenticationPhoneNumber', 'phone_number': self.phone})

	def authorizationStateWaitEmailAddress(self, client: TelegramClient, value: any):
		# client.send({'@type': 'setAuthenticationEmailAddress', 'email_address': "nobody@gmail.com"})
		raise NotImplementedError()

	def authorizationStateWaitRegistration(self, client: TelegramClient, value: any):
		client.send({'@type': 'registerUser', 'first_name': "Herp", 'last_name': "Derp"})

	def authorizationStateWaitPassword(self, client: TelegramClient, value: any):
		client.send({'@type': 'checkAuthenticationPassword', 'password': "password"})

	def authorizationStateWaitCode(self, client: TelegramClient, value: any):
		client.send({'@type': 'checkAuthenticationCode', 'code': value})