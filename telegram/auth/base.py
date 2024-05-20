from telegram.client import TelegramClient

class AuthenticationScheme:
	def authorizationStateWaitTdlibParameters(self, client: TelegramClient):
		raise NotImplementedError()

	def authorizationStateWaitPhoneNumber(self, client: TelegramClient):
		raise NotImplementedError()

	def authorizationStateWaitEmailAddress(self, client: TelegramClient):
		raise NotImplementedError()

	def authorizationStateWaitEmailCode(self, client: TelegramClient):
		raise NotImplementedError()

	def authorizationStateWaitCode(self, client: TelegramClient):
		raise NotImplementedError()

	def authorizationStateWaitRegistration(self, client: TelegramClient):
		raise NotImplementedError()

	def authorizationStateWaitPassword(self, client: TelegramClient):
		raise NotImplementedError()