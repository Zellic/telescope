import re
from typing import Optional

from telegram.module import TelegramModule, OnEvent

TELEGRAM_CHAT_ID = 777000

def get_login_code(text):
	pattern = r"Login code: (\d+)"
	match = re.search(pattern, text, re.IGNORECASE)

	if match:
		return match.group(1)
	else:
		return None

class GetAuthCode(TelegramModule):
	def __init__(self):
		self.code = None
		self.timestamp = None

	def process_message(self, client, msg):
		text = msg['content']['text']['text']
		code = get_login_code(text)

		if(code is None):
			return

		if(self.code is None or msg['date'] > self.timestamp):
			self.timestamp = msg['date']
			self.code = code

	@OnEvent("updateChatLastMessage")
	async def updateChatLastMessage(self, client, event):
		if(event['chat_id'] != TELEGRAM_CHAT_ID):
			return

		self.process_message(client, event['last_message'])

	@OnEvent("messages")
	async def messages(self, client, event):
		for x in event['messages']:
			if (x['chat_id'] != TELEGRAM_CHAT_ID):
				continue

			self.process_message(client, x)

	# noinspection PyMethodMayBeStatic
	async def getAuthCode(self, client):
		await client.sendAwaitingReply({
			'@type': 'getChatHistory',
			'chat_id': TELEGRAM_CHAT_ID,
			'from_message_id': 0,
			'offset': -5,
			'limit': 5,
		})