from mainloop import MainLoop
from telegram.auth.api import APIAuth
from telegram.auth.schemes.staging import TelegramStaging
from telegram.client import TelegramClient
from telegram.tgmodules.getcode import GetAuthCode
from telegram.tgmodules.userinfo import UserInfo

def main():
	core = MainLoop()

	def testClientForClosure(phonenumber):
		scheme = TelegramStaging(phonenumber, core.API_ID, core.API_HASH, "accounts/" + phonenumber)
		return TelegramClient(APIAuth(phonenumber, scheme), [UserInfo(), GetAuthCode()])

	core.addClient(testClientForClosure(TelegramStaging.generate_phone()))

	core.mainLoop(testClientForClosure)

if __name__ == "__main__":
	main()