from typing import Optional

from database.accounttype import TelegramAccount
from mainloop import MainLoop
from telegram.auth.api import APIAuth
from telegram.auth.base import StaticSecrets
from telegram.auth.schemes.live import TelegramProduction
from telegram.client import TelegramClient
from telegram.tgmodules.getcode import GetAuthCode
from telegram.tgmodules.savecontacts import SaveContacts
from telegram.tgmodules.userinfo import UserInfo
from telegram.util import Environment

def main():
	core = MainLoop(Environment.Production)

	def clientForClosure(account: TelegramAccount):
		secrets = None if account.two_factor_password is None else StaticSecrets(account.two_factor_password)
		scheme = TelegramProduction(core.API_ID, core.API_HASH, "accounts/" + account.phone_number, secrets, True)
		return TelegramClient(APIAuth(account.phone_number, scheme), [
			UserInfo(account.phone_number, core.accounts, account.username),
			SaveContacts(core.db, account.phone_number),
			GetAuthCode()
		])

	async def onStart():
		for account in await core.accounts.getAccounts():
			await core.addClient(clientForClosure(account))

	core.mainLoop(onStart, clientForClosure)

if __name__ == "__main__":
	main()
