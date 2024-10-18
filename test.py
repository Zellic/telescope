from typing import Optional
from database.accounttype import TelegramAccount
from mainloop import MainLoop
from telegram.auth.api import APIAuth
from telegram.auth.base import StaticSecrets
from telegram.auth.schemes.development import TelegramDevelopment
from telegram.client import TelegramClient
from telegram.tgmodules.getcode import GetAuthCode
from telegram.tgmodules.userinfo import UserInfo
from telegram.util import Environment

def main():
    core = MainLoop(Environment.Development)

    def testClientForClosure(account: TelegramAccount):
        secrets = None if account.two_factor_password is None else StaticSecrets(account.two_factor_password)
        scheme = TelegramDevelopment(account.phone_number, core.API_ID, core.API_HASH, "accounts/" + account.phone_number, secrets)
        return TelegramClient(APIAuth(account.phone_number, scheme), [
            UserInfo(account.phone_number, core.accounts, account.username),
            GetAuthCode()
        ])

    async def onStart():
        for account in await core.accounts.getAccounts():
            await core.addClient(testClientForClosure(account))

    # core.addClient(testClientForClosure(TelegramDevelopment.generate_phone(), None, False))
    core.mainLoop(onStart, testClientForClosure)


if __name__ == "__main__":
    main()
