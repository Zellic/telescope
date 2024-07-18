import dataclasses
from typing import Optional

from telegram.module import TelegramModule, OnEvent

@dataclasses.dataclass
class UserInfoContainer:
	id: int
	first_name: str
	last_name: str
	username: Optional[str]

class UserInfo(TelegramModule):
	def __init__(self):
		self.info: Optional[UserInfoContainer] = None

	@OnEvent("updateAuthorizationState")
	async def updateAuthorizationState(self, client, event):
		if event['authorization_state']['@type'] != 'authorizationStateReady':
			return

		info = await client.sendAwaitingReply({'@type': 'getMe'})
		self.info = UserInfoContainer(
			info['id'],
			info['first_name'],
			info['last_name'],
			info['usernames']['editable_username'] if 'usernames' in info and info['usernames'] is not None else None
		)