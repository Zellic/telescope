from typing import Optional

from mainloop import MainLoop
from telegram.auth.api import APIAuth
from telegram.auth.base import StaticSecrets
from telegram.auth.schemes.live import TelegramProduction
from telegram.client import TelegramClient
from telegram.tgmodules.getcode import GetAuthCode
from telegram.tgmodules.savecontacts import SaveContacts
from telegram.tgmodules.userinfo import UserInfo

def main():
	core = MainLoop()

	def clientForClosure(phonenumber, username: Optional[str]=None, secrets: Optional[StaticSecrets]=None):
		scheme = TelegramProduction(core.API_ID, core.API_HASH, "accounts/" + phonenumber, secrets, True)
		return TelegramClient(APIAuth(phonenumber, scheme), [
			UserInfo(
				phonenumber,
				core.accounts,
				username,
			),
			SaveContacts(core.db, phonenumber),
			GetAuthCode()
		])

	for account in core.accounts.getAccounts():
		core.addClient(clientForClosure(
			account.phone_number,
			account.username,
			None if account.two_factor_password is None else StaticSecrets(account.two_factor_password)
		))

	core.mainLoop(clientForClosure)

if __name__ == "__main__":
	main()
