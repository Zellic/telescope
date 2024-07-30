from typing import Optional

from mainloop import MainLoop
from telegram.auth.api import APIAuth
from telegram.auth.schemes.staging import TelegramStaging
from telegram.client import TelegramClient
from telegram.tgmodules.getcode import GetAuthCode
from telegram.tgmodules.userinfo import UserInfo

def main():
	core = MainLoop()

	def testClientForClosure(phonenumber, username: Optional[str], isInDB: bool):
		scheme = TelegramStaging(phonenumber, core.API_ID, core.API_HASH, "accounts/" + phonenumber)
		return TelegramClient(APIAuth(phonenumber, scheme), [
			UserInfo(phonenumber, None if not isInDB else core.accounts, username),
			GetAuthCode()
		])

	for account in core.accounts.getAccounts():
		core.addClient(testClientForClosure(account.phone_number, account.username, True))

	# core.addClient(testClientForClosure(TelegramStaging.generate_phone(), None, False))
	core.mainLoop(lambda phone, username: testClientForClosure(phone, username, False))

if __name__ == "__main__":
	main()