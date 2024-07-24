import hashlib
from dataclasses import dataclass, field
from typing import Optional, Dict

from database.core import Database
from telegram.module import TelegramModule, OnEvent

# https://github.com/tdlib/td/blob/f35dea776cdaa8b986e2a634dfabf0dafe659be7/td/generate/scheme/td_api.tl#L993
@dataclass
class TelegramContact:
	"""Unique serial primary key for DB operations."""
	id: int = field(init=False, default=None)
	"""The user ID for this Telegram contact. Unique per zellic_user_id"""
	contact_id: int
	"""The source account phone number for this contact - one to many."""
	zellic_phone_number: str

	usernames: Optional[list[str]]
	phone_number: Optional[str]
	first_name: Optional[str]
	last_name: Optional[str]

	"""The user is a close friend of the current user; implies that the user is a contact"""
	is_close_friend: bool

	"""The user is a contact of the current user."""
	is_contact: bool

	"""True, if many users reported this user as a fake account."""
	is_fake: bool

	"""The user is a contact of the current user and the current user is a contact of the user."""
	is_mutual_contact: bool

	"""True, if the user is a Telegram Premium user"""
	is_premium: bool

	"""True, if many users reported this user as a scam."""
	is_scam: bool

	"""	True, if the user is Telegram support account."""
	is_support: bool

	"""	True, if the user is verified."""
	is_verified: bool

	"""If false, the user is inaccessible, and the only information known about the user is inside this class. It
	can't be passed to any method except GetUser."""
	have_access: bool

	"""True, if the user may restrict new chats with non-contacts. Use canSendMessageToUser to check whether the
	current user can message the user or try to create a chat with them"""
	restricts_new_chats: bool

	"""If non-empty, it contains a human-readable description of the reason why access to this user must be restricted"""
	restriction_reason: Optional[str]

	hash: str = field(init=False)

	def __post_init__(self):
		self.hash = self.generate_hash()

	def generate_hash(self) -> str:
		data = (
			str(self.contact_id) +
			str(self.zellic_phone_number) +
			(''.join(self.usernames) if self.usernames else '') +
			(self.phone_number or '') +
			(self.first_name or '') +
			(self.last_name or '') +
			str(self.is_close_friend) +
			str(self.is_contact) +
			str(self.is_fake) +
			str(self.is_mutual_contact) +
			str(self.is_premium) +
			str(self.is_scam) +
			str(self.is_support) +
			str(self.is_verified) +
			str(self.have_access) +
			str(self.restricts_new_chats) +
			(self.restriction_reason or '')
		)
		return hashlib.md5(data.encode()).hexdigest()


	def to_db_tuple(self) -> tuple:
		return (
			self.contact_id,
			self.zellic_phone_number,
			self.hash,
			self.usernames,
			self.phone_number,
			self.first_name,
			self.last_name,
			self.is_close_friend,
			self.is_contact,
			self.is_fake,
			self.is_mutual_contact,
			self.is_premium,
			self.is_scam,
			self.is_support,
			self.is_verified,
			self.have_access,
			self.restricts_new_chats,
			self.restriction_reason
		)

insert_sql = """
INSERT INTO telegram_contacts (
	contact_id, zellic_phone_number, hash, usernames, phone_number, first_name, last_name, 
	is_close_friend, is_contact, is_fake, is_mutual_contact, 
	is_premium, is_scam, is_support, is_verified, 
	have_access, restricts_new_chats, restriction_reason
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (hash) DO NOTHING;
"""


create_table_sql = """
CREATE TABLE IF NOT EXISTS telegram_contacts (
    id SERIAL PRIMARY KEY,
    contact_id BIGINT,
    zellic_phone_number TEXT,
    hash TEXT UNIQUE,
    usernames TEXT[],
    phone_number TEXT,
    first_name TEXT,
    last_name TEXT,
    is_close_friend BOOLEAN,
    is_contact BOOLEAN,
    is_fake BOOLEAN,
    is_mutual_contact BOOLEAN,
    is_premium BOOLEAN,
    is_scam BOOLEAN,
    is_support BOOLEAN,
    is_verified BOOLEAN,
    have_access BOOLEAN,
    restricts_new_chats BOOLEAN,
    restriction_reason TEXT
);
"""

def truthyOrNull(thing):
	if(thing):
		return thing
	else:
		return None

class SaveContacts(TelegramModule):
	def __init__(self, db: Database, our_phone_number):
		self.db = db
		self.user_records: Dict[int, TelegramContact] = {}
		result = self.db.execute(create_table_sql)
		if(not result.success):
			raise Exception(f"Failed to create contacts table: {result.error_message}")
		self.our_phone_number = our_phone_number

	@OnEvent("updateAuthorizationState")
	async def updateAuthorizationState(self, client, event):
		if event['authorization_state']['@type'] != 'authorizationStateReady':
			return

		# ideally we'd iterate and make sure we get everyone, but I'm worried about the telegram API getting
		# mad at us
		await client.sendAwaitingReply({'@type': 'getChats', 'limit': 100})

	@OnEvent("updateUser")
	async def updateUser(self, client, event):
		user = event['user']

		if(user['type']['@type'] != "userTypeRegular"):
			return

		usernames = user.get('usernames', {'active_usernames': []})['active_usernames']

		if(user.get('username', None)):
			usernames.append(user['username'])

		if(len(usernames) > 0):
			usernames = list(set(usernames))
		else:
			usernames = None

		ours = TelegramContact(
			user['id'],
			self.our_phone_number,
			usernames,
			truthyOrNull(user.get('phone_number', None)),
			truthyOrNull(user.get('first_name', None)),
			truthyOrNull(user.get('last_name', None)),
			user['is_close_friend'],
			user['is_contact'],
			user['is_fake'],
			user['is_mutual_contact'],
			user['is_premium'],
			user['is_scam'],
			user['is_support'],
			user['is_verified'],
			user['have_access'],
			user['restricts_new_chats'],
			truthyOrNull(user.get('restriction_reason', None)),
		)

		self.user_records[event['user']['id']] = ours

	@OnEvent("updateNewChat")
	async def updateNewChat(self, client, event):
		chat = event['chat']

		if(chat['type']['@type'] != "chatTypePrivate"):
			return

		user = self.user_records.get(chat['type']['user_id'], None)

		if(user is None):
			return

		print("DM with user: " + repr(user))
		result = self.db.execute(insert_sql, user.to_db_tuple())
		if(not result.success):
			raise Exception(f"Failed to update contact table: {result.error_message}")