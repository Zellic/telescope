from telegram.auth.base import AuthenticationScheme
from telegram.client import TelegramClient

class TelegramProduction(AuthenticationScheme):
	def __init__(self, api_id: str, api_hash: str, db_directory: str, use_message_database=False):
		self.api_id = api_id
		self.api_hash = api_hash
		self.db_directory = db_directory
		self.use_message_database = use_message_database

	def authorizationStateWaitTdlibParameters(self, client: TelegramClient):
		client.send({
			'@type': 'setTdlibParameters',
			'database_directory': self.db_directory, #'accounts/' + value.phone,
			'use_message_database': self.use_message_database,
			'use_secret_chats': False,
			'api_id': self.api_id,
			'api_hash': self.api_hash,
			'system_language_code': 'en',
			'device_model': 'Desktop',
			'application_version': '0.1'
		})

	def authorizationStateReady(self, client: TelegramClient):
		pass

	def authorizationStateClosed(self, client: TelegramClient):
		pass

	def authorizationStateWaitPhoneNumber(self, client: TelegramClient, value: any):
		client.send({'@type': 'setAuthenticationPhoneNumber', 'phone_number': value})

	def authorizationStateWaitEmailAddress(self, client: TelegramClient, value: any):
		client.send({'@type': 'setAuthenticationEmailAddress', 'email_address': value})

	def authorizationStateWaitPassword(self, client: TelegramClient, value: any):
		client.send({'@type': 'checkAuthenticationPassword', 'password': value})

	def authorizationStateWaitEmailCode(self, client: TelegramClient, value: any):
		client.send({'@type': 'checkAuthenticationEmailCode',
		             'code': {'@type': 'emailAddressAuthenticationCode', 'code': value}})

	def authorizationStateWaitCode(self, client: TelegramClient, value: any):
		client.send({'@type': 'checkAuthenticationCode', 'code': value})