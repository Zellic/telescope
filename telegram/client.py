from telegram.tdlib import TDLib

class TelegramClient:
	def __init__(self):
		self.tdlib = TDLib()
		self.client_id = self.tdlib.create_client_id()

	def send(self, query):
		self.tdlib.send(self.client_id, query)

	def receive(self):
		return self.tdlib.receive()