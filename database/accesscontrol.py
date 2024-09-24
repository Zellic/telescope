import sys
from dataclasses import dataclass
from enum import Enum
from typing import List, Set, ClassVar, Optional

from database.core import Database


class Privilege(Enum):
    VIEW = "view"
    EDIT_TWO_FACTOR_PASSWORD = "edit_two_factor_password"
    JOIN_GROUP = "join_group"
    LOGIN = "login"
    MANAGE_CONNECTION_STATE = "manage_connection_state"
    REMOVE_ACCOUNT = "remove_account"

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
    roles: List[str]
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

    async def init(self):
        for table in TABLES:
            result = await self.db.execute(table.CREATE_TABLE)

            if(not result.success):
                raise Exception(f"Failed to create {table.__name__} table: {result.error_message}")

    async def get_user(self, email: str) -> Optional[User]:
        query = "SELECT * FROM users WHERE email = %s"
        result = await self.db.execute(query, (email,))

        if(result.success == False):
            sys.stderr.write(f"Failed get_roles_for_user query: {result.error_message}")
            return None

        if (len(result.data) == 0):
            return None

        return User(*result.data[0])

    async def get_privileges_for_pair(self, roles: List[int], groups: List[int]) -> List[str]:
        query = """
SELECT ARRAY_AGG(DISTINCT privilege) AS all_privileges
FROM (
    SELECT UNNEST(privileges) AS privilege
    FROM telegram_privileges
    WHERE role_id IN (SELECT UNNEST(%s::int[]))
    AND group_id IN (SELECT UNNEST(%s::int[]))
) AS subquery;
"""
        result = await self.db.execute(query, (roles, groups,))

        if(result.success == False):
            sys.stderr.write(f"Failed get_privileges_for_pair query: {result.error_message}")
            return []

        if (len(result.data) == 0):
            return []

        return result.data[0][0]