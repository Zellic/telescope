from mainloop import MainLoop
from telegram.auth.api import APIAuth
from telegram.auth.schemes.live import TelegramProduction
from telegram.client import TelegramClient
from telegram.tgmodules.getcode import GetAuthCode
from telegram.tgmodules.savecontacts import SaveContacts
from telegram.tgmodules.userinfo import UserInfo

def main():
	core = MainLoop()

	def clientForClosure(phonenumber):
		scheme = TelegramProduction(core.API_ID, core.API_HASH, "accounts/" + phonenumber, True)
		return TelegramClient(APIAuth(phonenumber, scheme), [UserInfo(), SaveContacts(core.db, phonenumber), GetAuthCode()])

	for account in core.accounts.getAccounts():
		core.addClient(clientForClosure(account.phone_number))

	core.mainLoop(clientForClosure)

if __name__ == "__main__":
	main()