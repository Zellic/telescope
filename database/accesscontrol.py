import sys
from dataclasses import dataclass
from enum import Enum
from typing import List, Set, ClassVar, Optional, Any

from database.accounttype import TelegramAccount
from database.core import Database

class Privilege(Enum):
    VIEW = "view"
    EDIT_TWO_FACTOR_PASSWORD = "edit_two_factor_password"
    # JOIN_GROUP = "join_group"
    LOGIN = "login"
    MANAGE_CONNECTION_STATE = "manage_connection_state"
    REMOVE_ACCOUNT = "remove_account"

DEFAULT_PRIVILEGE_SET_FOR_OWN_ACCOUNT = {
    Privilege.VIEW,
    Privilege.EDIT_TWO_FACTOR_PASSWORD,
    Privilege.LOGIN,
    Privilege.MANAGE_CONNECTION_STATE,
}

@dataclass
class Role:
    id: int
    name: str
    CREATE_TABLE: ClassVar[str] = """
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);
"""

@dataclass
class TelegramGroup:
    id: int
    name: str
    CREATE_TABLE: ClassVar[str] = """
CREATE TABLE IF NOT EXISTS telegram_groups (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);
"""

@dataclass
class User:
    id: int
    email: str
    roles: List[int]
    CREATE_TABLE: ClassVar[str] = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    roles INTEGER[]
);
"""

@dataclass
class TelegramPrivilegeSet:
    group_id: int
    role_id: int
    privileges: List[str]
    CREATE_TABLE: ClassVar[str] = """
CREATE TABLE IF NOT EXISTS telegram_privileges (
    group_id INTEGER REFERENCES telegram_groups(id) ON DELETE CASCADE NOT NULL,
    role_id INTEGER REFERENCES roles(id) ON DELETE CASCADE NOT NULL,
    privileges TEXT[] NOT NULL,
    PRIMARY KEY (group_id, role_id)
);
"""

TABLES = {Role, TelegramGroup, User, TelegramPrivilegeSet}

class UserPrivilegeManager:
    def __init__(self, db: Database):
        self.db = db
        self.cache = {}

    async def init(self):
        for table in TABLES:
            result = await self.db.execute(table.CREATE_TABLE)
            if not result.success:
                raise Exception(f"Failed to create {table.__name__} table: {result.error_message}")

        await self.reload_cache()

    async def reload_cache(self):
        self.cache = {
            'roles': await self._load_roles(),
            'groups': await self._load_groups(),
            'privileges': {(x.group_id, x.role_id): x for x in (await self._load_privileges())}
        }

    async def _load_roles(self) -> List[Role]:
        query = "SELECT * FROM roles"
        result = await self.db.execute(query)
        return [Role(*x) for x in result.data] if result.success else []

    async def _load_groups(self) -> List[TelegramGroup]:
        query = "SELECT * FROM telegram_groups"
        result = await self.db.execute(query)
        return [TelegramGroup(*x) for x in result.data] if result.success else []

    async def _load_privileges(self) -> List[TelegramPrivilegeSet]:
        query = "SELECT group_id, role_id, privileges FROM telegram_privileges"
        result = await self.db.execute(query)
        return [TelegramPrivilegeSet(*x) for x in result.data] if result.success else []

    async def get_user(self, email: str) -> Optional[User]:
        query = "SELECT * FROM users WHERE email = %s"
        result = await self.db.execute(query, (email,))

        if(result.success == False):
            sys.stderr.write(f"Failed get_roles_for_user query: {result.error_message}")
            return None

        if (len(result.data) == 0):
            return None

        return User(*result.data[0])

    def get_privileges_for_pair(self, roles: List[int], groups: List[int]) -> set[Any]:
        all_privileges = set()
        for role in roles:
            for group in groups:
                privset = self.cache['privileges'].get((group, role), [])
                all_privileges.update(privset.privileges)
        return all_privileges

    def get_privileges_on_account(self, user: User, account: TelegramAccount) -> set[str]:
        extra = DEFAULT_PRIVILEGE_SET_FOR_OWN_ACCOUNT if account.email and user.email == account.email else set()
        extra.update(self.get_privileges_for_pair(user.roles, account.groups))
        return extra