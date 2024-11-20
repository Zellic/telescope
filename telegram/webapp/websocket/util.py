from quart import current_app

from telegram.client import TelegramClient
from telegram.tgmodules.getcode import GetAuthCode
from telegram.tgmodules.userinfo import UserInfo
from database.accesscontrol import UserPrivilegeManager, Privilege
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from telegram.webapp.webapp import WebApp

# DO NOT CALL THIS FUNCTION OUTSIDE OF REQUESTS !
def get_webapp() -> 'WebApp':
    return current_app.config.get('webapp')

async def tg_client_blob(webapp: 'WebApp', user: TelegramClient):
    info_module = next((x for x in user._modules if isinstance(x, UserInfo)), None)
    info = None if info_module is None else info_module.info

    code_module = next((x for x in user._modules if isinstance(x, GetAuthCode)), None)

    # TODO: should probably batch this...
    # ^ actually when we couple accounts with db objects they will be cached
    account = await webapp.get_tg_account(user.auth.phone)
    privileges = await webapp.privilegesFor(None, account)

    if Privilege.VIEW not in privileges:
        return None

    return {
        "name": None if info is None or info.first_name is None or info.last_name is None else info.first_name + " " + info.last_name,
        "username": None if info is None else info.username,
        "phone": user.auth.phone,
        "email": None if account is None else account.email,
        "comment": None if account is None else account.comment,
        "lastCode": None if code_module is None or code_module.code is None else {
            "value": int(code_module.code),
            "date": code_module.timestamp,
        },
        "two_factor_pass_is_set": False if account is None else account.two_factor_password is not None,
        "two_factor_protected": None if info is None else info.has_2fa,
        "status": {
            "stage": user.auth.status.name,
            "inputRequired": user.auth.status.requiresInput,
            "error": user.auth.status.error if hasattr(user.auth.status, "error") else None,
        },
        "privileges": [x.value for x in privileges],
    }