import sys

from telegram.client import TelegramClient
from telegram.auth.testaccount import TestAccount

def main():
	client = TelegramClient()

	# log verbosity: errors
	print(client.tdlib.td_execute({'@type': 'setLogVerbosityLevel', 'new_verbosity_level': 1, '@extra': 1.01234}))

	# Example request
	# print(client.tdlib.td_execute(
	# 	{'@type': 'getTextEntities', 'text': '@telegram /test_command https://telegram.org telegram.me',
	# 	 '@extra': ['5', 7.0, 'a']}))

	# Start the client by sending a request to it
	client.send({'@type': 'getOption', 'name': 'version', '@extra': 1.01234})

	auth = TestAccount()

	while True:
		event = client.receive()
		if event:
			if event['@type'] == 'updateAuthorizationState':
				auth_state = event['authorization_state']

				if auth_state['@type'] == 'authorizationStateClosed':
					print("Authorization failed.")
					break
				elif auth_state['@type'] == 'authorizationStateReady':
					print("Authorization successful.")
					pass
				else:
					method = getattr(auth, auth_state['@type'], None)

					if method is None:
						print(f"Unimplemented authorization state: {auth_state['@type']}")
						raise NotImplementedError()

					method(client)
			elif event['@type'] == 'updateConnectionState':
				if event['state']['@type'] == 'connectionStateReady':
					client.send({'@type': 'getContacts'})

			print(str(event).encode('utf-8'))
			sys.stdout.flush()


if __name__ == "__main__":
	main()
