from dataclasses import dataclass
from typing import Optional, List, Any

import aiopg
import psycopg2
from aiopg import Pool
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.pool import SimpleConnectionPool
from psycopg2.sql import SQL, Identifier

def _parse_dbname_from_dsn(dsn):
	try:
		params = psycopg2.extensions.parse_dsn(dsn)
		return params.get('dbname')
	except Exception as e:
		raise ValueError(f"Error parsing DSN: {str(e)}")

@dataclass
class QueryResult:
	success: bool
	data: Optional[List[Any]] = None
	error_message: Optional[str] = None
	error_code: Optional[str] = None
	query: Optional[str] = None

class Database:
	def __init__(self, dsn, minconn=1, maxconn=10):
		self.dsn = dsn
		self.minconn = minconn
		self.maxconn = maxconn
		self.dbname = _parse_dbname_from_dsn(dsn)

		if(self.dbname is None):
			raise Exception("Must specify dbname in database DSN")

		self._ensure_database_exists()
		self.pool: Pool = None

	# this already used psycopg2 and aiopg uses psycopg2 under the hood so I'm just leaving it
	def _ensure_database_exists(self):
		# to create a database you must connect to the postgres database, so we adjust the DSN
		default_dsn = self.dsn.replace(f"dbname={self.dbname}", "dbname=postgres")

		if(default_dsn == self.dsn):
			raise Exception("Couldn't adjust DSN for default database...")

		conn = psycopg2.connect(default_dsn)
		conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

		def database_exists():
			cur = conn.cursor()
			cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (self.dbname,))
			return cur.fetchone() is not None

		def create_database():
			cur = conn.cursor()
			cur.execute(SQL("CREATE DATABASE {}").format(Identifier(self.dbname)))
			cur.close()

		try:
			if not database_exists():
				create_database()
				print(f"Database {self.dbname} created successfully.")
			else:
				print(f"Database {self.dbname} already exists.")
		finally:
			conn.close()

	async def execute(self, query, params=None):
		if(self.pool is None):
			self.pool = await aiopg.create_pool(self.dsn, minsize=self.minconn, maxsize=self.maxconn)

		async with self.pool.acquire() as conn:
			async with conn.cursor() as cursor:
				try:
					await cursor.execute(query, params)
					try:
						data = await cursor.fetchall()
						return QueryResult(success=True, data=data)
					except psycopg2.ProgrammingError as e:
						if e.pgcode is None:
							return QueryResult(success=True, data=None)
						else:
							return QueryResult(
								success=False,
								error_message=str(e),
								error_code=e.pgcode,
								query=query
							)
				except psycopg2.Error as e:
					await conn.rollback()
					return QueryResult(
						success=False,
						error_message=e.pgerror,
						error_code=e.pgcode,
						query=query
					)

	def close_all(self):
		if self.pool is not None:
			self.pool.close()