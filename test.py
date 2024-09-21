from typing import Optional

from mainloop import MainLoop
from telegram.auth.api import APIAuth
from telegram.auth.base import StaticSecrets
from telegram.auth.schemes.staging import TelegramStaging
from telegram.client import TelegramClient
from telegram.tgmodules.getcode import GetAuthCode
from telegram.tgmodules.userinfo import UserInfo
from telegram.util import Environment

def main():
	core = MainLoop(Environment.Staging)

	def testClientForClosure(phonenumber, username: Optional[str]=None, secrets: Optional[StaticSecrets]=None):
		scheme = TelegramStaging(phonenumber, core.API_ID, core.API_HASH, "accounts/" + phonenumber, secrets)
		return TelegramClient(APIAuth(phonenumber, scheme), [
			UserInfo(phonenumber, core.accounts, username),
			GetAuthCode()
		])

	async def onStart():
		for account in await core.accounts.getAccounts():
			await core.addClient(testClientForClosure(
				account.phone_number,
				account.username,
				None if account.two_factor_password is None else StaticSecrets(account.two_factor_password)
			))

	# core.addClient(testClientForClosure(TelegramStaging.generate_phone(), None, False))
	core.mainLoop(onStart, testClientForClosure)

if __name__ == "__main__":
	main()