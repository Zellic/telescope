import sys

from database.core import Database, QueryResult
import re
from typing import List, Optional, NamedTuple

from dataclasses import dataclass

from database.pgcrypt import encrypt_string, decrypt_string

create_table_sql = """
CREATE TABLE IF NOT EXISTS telegram_accounts (
    id SERIAL PRIMARY KEY,
    phone_number TEXT NOT NULL UNIQUE,
    username TEXT,
    email TEXT,
    comment TEXT,
    two_factor_password TEXT
);
"""

@dataclass
class Account:
	id: int
	phone_number: str
	username: Optional[str]
	email: Optional[str]
	comment: Optional[str]
	two_factor_password: Optional[str]

class AddAccountResult(NamedTuple):
	success: bool
	error_message: Optional[str]

class AccountManager:
	def __init__(self, db: Database, encryption_key: str):
		self.db = db
		self.encryption_key = encryption_key
		result = self.db.execute(create_table_sql)
		if(not result.success):
			raise Exception(f"Failed to create accounts table: {result.error_message}")

	def _make_account_decrypted(self, *data):
		ret = Account(*data)
		# noinspection PyBroadException
		if(ret.two_factor_password is not None):
			try:
				ret.two_factor_password = decrypt_string(ret.two_factor_password, self.encryption_key)
			except:
				sys.stderr.write(f"[!] Failed to decrypt two factor password for account id: {ret.id}, phone: {ret.phone_number}\n")
		return ret

	def getAccounts(self) -> List[Account]:
		query = "SELECT id, phone_number, username, email, comment, two_factor_password FROM telegram_accounts"
		results = self.db.execute(query)

		if(results.success == False):
			raise Exception("Failed to fetch accounts.")

		return [self._make_account_decrypted(*row) for row in results.data]

	def add_account(self, phone_number: str, email: Optional[str] = None, comment: Optional[str] = None, staging: bool = False) -> AddAccountResult:
		phone_length = 10 if staging else 11
		if not re.match(f'^\\d{{{phone_length}}}$', phone_number):
			return AddAccountResult(False, "Phone number must be exactly 11 digits")

		# todo: use a proper library
		if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
			return AddAccountResult(False, "Invalid email format")

		if comment and (len(comment) < 1 or len(comment) > 300):
			return AddAccountResult(False, "Comment must be between 1 and 300 characters")

		insert_query = """
        INSERT INTO telegram_accounts (phone_number, email, comment)
        VALUES (%s, %s, %s)
        """

		try:
			result = self.db.execute(insert_query, (phone_number, email, comment))
			if result.success:
				return AddAccountResult(True, None)
			else:
				return AddAccountResult(False, f"Failed to insert account: {result.error_message}")
		except Exception as e:
			return AddAccountResult(False, f"Database error: {str(e)}")

	def set_username(self, phone_number: str, username: str) -> None:
		insert_query = """
		UPDATE telegram_accounts
		SET username = %s
		WHERE phone_number = %s;
        """

		try:
			self.db.execute(insert_query, (username, phone_number))
		except Exception as e:
			print(f"Failed to set username: {e}")

	def set_two_factor_password(self, phone_number: str, password: str) -> QueryResult:
		insert_query = """
		UPDATE telegram_accounts
		SET two_factor_password = %s
		WHERE phone_number = %s;
        """

		try:
			encrypted_password = encrypt_string(password, self.encryption_key)
		except:
			raise Exception(f"Failed to encrypt two factor password for account with phone number: {phone_number}")

		try:
			return self.db.execute(insert_query, (encrypted_password, phone_number))
		except Exception as e:
			print(f"Failed to set two factor password: {e}")

	def get_account(self, phone_number: str) -> Optional[Account]:
		query = "SELECT id, phone_number, username, email, comment, two_factor_password FROM telegram_accounts WHERE phone_number = %s"
		result = self.db.execute(query, (phone_number,))

		if(result.success == False or len(result.data) == 0):
			return None

		return self._make_account_decrypted(*result.data[0])

	def delete_account(self, phone_number: str) -> QueryResult:
		query = "DELETE FROM telegram_accounts WHERE phone_number = %s"
		result = self.db.execute(query, (phone_number,))

		return result