import random
from telegram.auth.base import AuthenticationScheme
from telegram.client import TelegramClient

class ProductionWithPrompt(AuthenticationScheme):
	def __init__(self, phone, api_id, api_hash):
		self.phone = phone
		self.api_id = api_id
		self.api_hash = api_hash

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

	def authorizationStateWaitPhoneNumber(self, client: TelegramClient):
		client.send({'@type': 'setAuthenticationPhoneNumber', 'phone_number': self.phone})

	def authorizationStateWaitEmailAddress(self, client: TelegramClient):
		# client.send({'@type': 'setAuthenticationEmailAddress', 'email_address': "nobody@gmail.com"})
		raise NotImplementedError()

	def authorizationStateWaitPassword(self, client: TelegramClient):
		password = input(f'[{self.phone}] Password: ')
		client.send({'@type': 'checkAuthenticationPassword', 'password': password})

	def authorizationStateWaitEmailCode(self, client: 'TelegramClient'):
		code = input(f'[{self.phone}] Email authentication code: ')
		client.send({'@type': 'checkAuthenticationEmailCode',
		             'code': {'@type': 'emailAddressAuthenticationCode', 'code': code}})

	def authorizationStateWaitCode(self, client: 'TelegramClient'):
		code = input(f'[{self.phone}] Authentication code: ')
		client.send({'@type': 'checkAuthenticationCode', 'code': code})