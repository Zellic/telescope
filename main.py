import asyncio
import os

from database.accounts import AccountManager
from database.core import Database
from mainloop import MainLoop
from telegram.auth.api import APIAuth
from telegram.auth.schemes.live import TelegramProduction
from telegram.auth.schemes.staging import TelegramStaging
from telegram.client import TelegramClient
from telegram.manager import TelegramClientManager
from telegram.tgmodules.savecontacts import SaveContacts
from telegram.webapp import create_webapp
from telegram.tgmodules.getcode import GetAuthCode
from telegram.tgmodules.userinfo import UserInfo

def main():
	core = MainLoop()

	def clientForClosure(phonenumber):
		scheme = TelegramProduction(core.API_ID, core.API_HASH, "accounts/" + phonenumber, True)
		return TelegramClient(APIAuth(phonenumber, scheme), [UserInfo(), SaveContacts(core.db, phonenumber), GetAuthCode()])

	for account in core.accounts.getAccounts():
		core.addClient(clientForClosure(account.phone_number))

	# noinspection PyProtectedMember
	core.mainLoop()

if __name__ == "__main__":
	main()