from telegram.auth.base import AuthenticationProvider, AuthenticationScheme
from telegram.client import TelegramClient

class ProductionWithPrompt(AuthenticationProvider):
	def __init__(self, scheme: AuthenticationScheme):
		self.scheme = scheme

	def authorizationStateWaitTdlibParameters(self, client: TelegramClient):
		self.scheme.authorizationStateWaitTdlibParameters(client)

	def authorizationStateWaitPhoneNumber(self, client: TelegramClient):
		value = input(f'Phone: ')
		self.scheme.authorizationStateWaitPhoneNumber(client, value)

	def authorizationStateWaitEmailAddress(self, client: TelegramClient):
		value = input(f'Email: ')
		self.scheme.authorizationStateWaitEmailAddress(client, value)

	def authorizationStateWaitPassword(self, client: TelegramClient):
		value = input(f'Password: ')
		self.scheme.authorizationStateWaitPassword(client, value)

	def authorizationStateWaitEmailCode(self, client: 'TelegramClient'):
		value = input(f'Email: ')
		self.scheme.authorizationStateWaitEmailCode(client, value)

	def authorizationStateWaitCode(self, client: 'TelegramClient'):
		value = input(f'Code: ')
		self.scheme.authorizationStateWaitCode(client, value)