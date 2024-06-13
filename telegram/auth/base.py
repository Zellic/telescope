class AuthenticationScheme:
	def authorizationStateFailed(self, client: 'TelegramClient'):
		pass

	def authorizationStateReady(self, client: 'TelegramClient'):
		pass

	def authorizationStateWaitTdlibParameters(self, client: 'TelegramClient'):
		raise NotImplementedError()

	def authorizationStateWaitPhoneNumber(self, client: 'TelegramClient'):
		raise NotImplementedError()

	def authorizationStateWaitEmailAddress(self, client: 'TelegramClient'):
		raise NotImplementedError()

	def authorizationStateWaitEmailCode(self, client: 'TelegramClient'):
		raise NotImplementedError()

	def authorizationStateWaitCode(self, client: 'TelegramClient'):
		raise NotImplementedError()

	def authorizationStateWaitRegistration(self, client: 'TelegramClient'):
		raise NotImplementedError()

	def authorizationStateWaitPassword(self, client: 'TelegramClient'):
		raise NotImplementedError()