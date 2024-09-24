from dataclasses import dataclass
from typing import Optional, List

# prevent circular import
@dataclass
class TelegramAccount:
	id: int
	phone_number: str
	username: Optional[str]
	email: Optional[str]
	comment: Optional[str]
	two_factor_password: Optional[str]
	groups: Optional[List[int]]