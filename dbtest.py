import asyncio, sys

from database.accesscontrol import User, Role, UserPrivilegeManager
from database.core import Database

async def main():
	db = Database(r"""user=postgres dbname=telescope_staging host=35.192.191.179 password=e@'^A$#gJQZT~&t(""")

	# await db.execute(Role.CREATE_TABLE)
	# print(await db.execute("INSERT INTO roles (name) VALUES ('test1')"))
	# print(await db.execute("INSERT INTO roles (name) VALUES ('test2')"))
	# await db.execute(User.CREATE_TABLE)
	# await db.execute("INSERT INTO users (email, roles) VALUES ('asdf@whatever.com', '{1, 2}')")
	# print(await db.execute("SELECT roles FROM users WHERE email = %s", ("asdf@whatever.com",)))
	rbac = UserPrivilegeManager(db)
	await rbac.init()
	print(rbac.get_privileges_for_pair([1,2], [1,2]))
	print(await rbac.get_or_create_user("test2@lol.com"))

	await db.close_all()
#
if __name__ == "__main__":
	# make aiopg work on windows
	if sys.version_info >= (3, 8) and sys.platform.lower().startswith("win"):
		asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

	asyncio.run(main())