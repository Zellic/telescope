import sys
from tdlib import TDLib

class TelegramClient:
	def __init__(self):
		self.tdlib = TDLib()
		self.client_id = self.tdlib.create_client_id()

	def send(self, query):
		self.tdlib.send(self.client_id, query)

	def receive(self):
		return self.tdlib.receive()


def main():
	client = TelegramClient()

	# Setting TDLib log verbosity level to 1 (errors)
	print(client.tdlib.td_execute({'@type': 'setLogVerbosityLevel', 'new_verbosity_level': 1, '@extra': 1.01234}))

	# Example request
	print(client.tdlib.td_execute(
		{'@type': 'getTextEntities', 'text': '@telegram /test_command https://telegram.org telegram.me',
		 '@extra': ['5', 7.0, 'a']}))

	# Start the client by sending a request to it
	client.send({'@type': 'getOption', 'name': 'version', '@extra': 1.01234})

	while True:
		event = client.receive()
		if event:
			if event['@type'] == 'updateAuthorizationState':
				auth_state = event['authorization_state']

				if auth_state['@type'] == 'authorizationStateClosed':
					break

				if auth_state['@type'] == 'authorizationStateWaitTdlibParameters':
					client.send({'@type': 'setTdlibParameters',
					             'database_directory': 'tdlib',
					             'use_message_database': True,
					             'use_secret_chats': True,
					             'api_id': 94575,
					             'api_hash': 'a3406de8d171bb422bb6ddf3bbd800e2',
					             'system_language_code': 'en',
					             'device_model': 'Desktop',
					             'application_version': '1.0'})

				if auth_state['@type'] == 'authorizationStateWaitPhoneNumber':
					phone_number = input('Please enter your phone number: ')
					client.send({'@type': 'setAuthenticationPhoneNumber', 'phone_number': phone_number})

				if auth_state['@type'] == 'authorizationStateWaitEmailAddress':
					email_address = input('Please enter your email address: ')
					client.send({'@type': 'setAuthenticationEmailAddress', 'email_address': email_address})

				if auth_state['@type'] == 'authorizationStateWaitEmailCode':
					code = input('Please enter the email authentication code you received: ')
					client.send({'@type': 'checkAuthenticationEmailCode',
					             'code': {'@type': 'emailAddressAuthenticationCode', 'code': code}})

				if auth_state['@type'] == 'authorizationStateWaitCode':
					code = input('Please enter the authentication code you received: ')
					client.send({'@type': 'checkAuthenticationCode', 'code': code})

				if auth_state['@type'] == 'authorizationStateWaitRegistration':
					first_name = input('Please enter your first name: ')
					last_name = input('Please enter your last name: ')
					client.send({'@type': 'registerUser', 'first_name': first_name, 'last_name': last_name})

				if auth_state['@type'] == 'authorizationStateWaitPassword':
					password = input('Please enter your password: ')
					client.send({'@type': 'checkAuthenticationPassword', 'password': password})

			print(str(event).encode('utf-8'))
			sys.stdout.flush()


if __name__ == "__main__":
	main()
