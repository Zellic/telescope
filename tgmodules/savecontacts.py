from telegram.module import TelegramModule, OnEvent

class SaveContacts(TelegramModule):
	def __init__(self, db):
		self.db = db
		self.user_records = {}

	@OnEvent("updateConnectionState")
	async def updateConnectionState(self, client, event):
		if event['state']['@type'] != 'connectionStateReady':
			return

		# ideally we'd iterate and make sure we get everyone, but I'm worried about the telegram API getting
		# mad at us
		await client.sendAwaitingReply({'@type': 'getChats', 'limit': 100})

	@OnEvent("updateUser")
	async def updateUser(self, client, event):
		self.user_records[event['user']['id']] = event['user']

	@OnEvent("updateNewChat")
	async def updateNewChat(self, client, event):
		chat = event['chat']

		if(chat['type']['@type'] != "chatTypePrivate"):
			return

		user = await client.sendAwaitingReply({'@type': 'getUser', 'user_id': chat['type']['user_id']})

		print("DM with user: " + self.user_records[chat['type']['user_id']]['first_name'])