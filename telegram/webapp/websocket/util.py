from quart import current_app

from telegram.client import TelegramClient
from telegram.tgmodules.getcode import GetAuthCode
from telegram.tgmodules.userinfo import UserInfo
from database.accesscontrol import UserPrivilegeManager, Privilege
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from telegram.webapp.webapp import WebApp

EXPORT_MESSAGE_TEXT_CHUNKS = [
    "Data export request",
    "we received a request from your account to export your Telegram data",
    "For security reasons, please confirm this request by pressing the Allow button at the bottom of this message using one of your mobile devices",
]

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

async def iterate_chat_history(client: TelegramClient, chat_id: int, from_message_id: int | None = None, offset: int | None = None, chunk_size: int = 30):
    query = {'@type': 'getChatHistory', 'chat_id': chat_id, 'from_message_id': from_message_id, 'offset': offset, 'limit': chunk_size}
    query_no_none = {k: v for k, v in query.items() if v is not None}

    while True:
        response = await client.sendAwaitingReply(query_no_none)
        messages = response['messages']
        for message in messages:
            yield message
        from_message_id = messages[-1]['id']

def is_export_request_message(message: dict) -> dict | None:
    try: 
        if message['@type'] != 'message':
            return None
        content = message['content']
        if content['@type'] != 'messageText':
            return None
        text = content['text']
        if text['@type'] != 'formattedText':
            return None
        message_text = text['text']
        if all(chunk in message_text for chunk in EXPORT_MESSAGE_TEXT_CHUNKS):
            return message
    except KeyError:
        return None

def get_export_request_approve_data(message: dict) -> str | None:
    try:
        reply_markup = message['reply_markup']
        if reply_markup['@type'] != 'replyMarkupInlineKeyboard':
            return None
        keyboard = reply_markup['rows']
        for row in keyboard:
            for button in row:
                if button['@type'] == 'inlineKeyboardButton' and button['text'] == "Allow":
                    return button['type']['data']
    except KeyError:
        return None