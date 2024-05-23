from telegram.module import TelegramModule, onEvent

class SaveContacts(TelegramModule):
	@onEvent("updateConnectionState")
	async def updateConnectionState(self, client, event):
		if event['state']['@type'] != 'connectionStateReady':
			return

		wot = await client.sendAwaitingReply({'@type': 'getChats', 'limit': 100})

		print("we did it reddit: " + repr(wot))