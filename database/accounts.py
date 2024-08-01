from database.core import Database, QueryResult
import re
from typing import List, Optional, NamedTuple

from dataclasses import dataclass

create_table_sql = """
CREATE TABLE IF NOT EXISTS telegram_accounts (
    id SERIAL PRIMARY KEY,
    phone_number TEXT NOT NULL UNIQUE,
    username TEXT,
    email TEXT,
    comment TEXT
);
"""

@dataclass
class Account:
	id: int
	phone_number: str
	username: Optional[str]
	email: Optional[str]
	comment: Optional[str]

class AddAccountResult(NamedTuple):
	success: bool
	error_message: Optional[str]

class AccountManager:
	def __init__(self, db: Database):
		self.db = db
		result = self.db.execute(create_table_sql)
		if(not result.success):
			raise Exception(f"Failed to create accounts table: {result.error_message}")

	def getAccounts(self) -> List[Account]:
		query = "SELECT id, phone_number, username, email, comment FROM telegram_accounts"
		results = self.db.execute(query)

		if(results.success == False):
			raise Exception("Failed to fetch accounts.")

		return [Account(*row) for row in results.data]

	def add_account(self, phone_number: str, email: Optional[str] = None, comment: Optional[str] = None) -> AddAccountResult:
		if not re.match(r'^\d{11}$', phone_number):
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

	def get_account(self, phone_number: str) -> Optional[Account]:
		query = "SELECT id, phone_number, username, email, comment FROM telegram_accounts WHERE phone_number = %s"
		result = self.db.execute(query, (phone_number,))

		if(result.success == False or len(result.data) == 0):
			return None

		return Account(*result.data[0])

	def delete_account(self, phone_number: str) -> QueryResult:
		query = "DELETE FROM telegram_accounts WHERE phone_number = %s"
		result = self.db.execute(query, (phone_number,))

		return result