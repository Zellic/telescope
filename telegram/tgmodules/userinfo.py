import dataclasses
import sys
from typing import Optional

from database.accounts import AccountManager
from telegram.module import TelegramModule, OnEvent

@dataclasses.dataclass
class UserInfoContainer:
	id: Optional[int]
	first_name: Optional[str]
	last_name: Optional[str]
	username: Optional[str]

	def db_username(self):
		if(self.username is not None):
			return self.username
		if(self.first_name is not None and self.last_name is not None):
			return self.first_name + " " + self.last_name
		return None

class UserInfo(TelegramModule):
	def __init__(self, phonenumber, accounts: Optional[AccountManager], username: Optional[str] = None):
		self.phonenumber = phonenumber
		self.info: Optional[UserInfoContainer] = None if username is None else UserInfoContainer(
			id=None,
			first_name=None,
			last_name=None,
			# TODO: there is a dumb thing here - username can be firstname+lastname if we had no username (see db_username)
			username=username
		)
		self.accounts = accounts

	@OnEvent("updateAuthorizationState")
	async def updateAuthorizationState(self, client, event):
		if event['authorization_state']['@type'] != 'authorizationStateReady':
			return

		old = self.info

		try:
			info = await client.sendAwaitingReply({'@type': 'getMe'})
		except Exception as ex:
			sys.stderr.write(f'getMe failed for {self.phonenumber}')
			return

		self.info = UserInfoContainer(
			info['id'],
			info['first_name'],
			info['last_name'],
			info['usernames']['editable_username'] if 'usernames' in info and info['usernames'] is not None else None
		)


		old_username = None if old is None else old.db_username()
		new_username = None if self.info is None or self.info.db_username() is None else self.info.db_username()
		if(self.accounts is not None and new_username is not None and old_username != new_username):
			await self.accounts.set_username(self.phonenumber, new_username)