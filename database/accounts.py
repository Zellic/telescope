from database.core import Database
import re
from typing import List, Optional, NamedTuple

from dataclasses import dataclass

create_table_sql = """
CREATE TABLE IF NOT EXISTS telegram_accounts (
    id SERIAL PRIMARY KEY,
    phone_number TEXT NOT NULL,
    email TEXT,
    comment TEXT
);
"""

@dataclass
class Account:
	id: int
	phone_number: str
	email: Optional[str]
	comment: Optional[str]


class AddAccountResult(NamedTuple):
	success: bool
	error_message: Optional[str]

class AccountManager:
	def __init__(self, db: Database):
		self.db = db
		self.db.execute(create_table_sql)

	def getAccounts(self) -> List[Account]:
		query = "SELECT id, phone_number, email, comment FROM telegram_accounts"
		results = self.db.execute(query)
		return [Account(*row) for row in results]

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
        SELECT %s, %s, %s
        WHERE NOT EXISTS (
            SELECT 1 FROM telegram_accounts WHERE phone_number = %s
        )
        RETURNING id
        """

		try:
			result = self.db.execute(insert_query, (phone_number, email, comment, phone_number))
			if result:
				return AddAccountResult(True, None)
			else:
				return AddAccountResult(False, "Account with this phone number already exists")
		except Exception as e:
			return AddAccountResult(False, f"Database error: {str(e)}")