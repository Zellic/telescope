import asyncio
import json
import re
import sys
from enum import Enum
from json import JSONDecodeError

from quart import websocket, Blueprint, request

from database.accesscontrol import Privilege
from sso.cloudflare import CloudflareAccessSSO
from sso.mock import MockSSO
from telegram.auth.api import ClientNotStarted
from telegram.auth.base import StaticSecrets
from telegram.auth.schemes.staging import TelegramStaging
from telegram.tgmodules.userinfo import UserInfo
from telegram.util import Environment
from telegram.webapp.websocket.util import tg_client_blob, get_webapp

websocket_bp = Blueprint('socket_bp', __name__)


class MessageSendType(str, Enum):
    SSO_START = "SSO_START"
    CLIENT_START = 'CLIENT_START'
    ADD_ACCOUNT_RESPONSE = "ADD_ACCOUNT_RESPONSE",
    ADD_TEST_ACCOUNT_RESPONSE = "ADD_TEST_ACCOUNT_RESPONSE"
    SUBMIT_VALUE_RESPONSE = "SUBMIT_VALUE_RESPONSE"
    DELETE_ACCOUNT_RESPONSE = "DELETE_ACCOUNT_RESPONSE"
    CONNECT_CLIENT_RESPONSE = "CONNECT_CLIENT_RESPONSE"
    DISCONNECT_CLIENT_RESPONSE = "DISCONNECT_CLIENT_RESPONSE"
    SET_PASSWORD_RESPONSE = "SET_PASSWORD_RESPONSE"


class MessageRecvType(str, Enum):
    ADD_ACCOUNT = "ADD_ACCOUNT"
    ADD_TEST_ACCOUNT = 'ADD_TEST_ACCOUNT'
    SUBMIT_VALUE = 'SUBMIT_VALUE'
    DELETE_ACCOUNT = "DELETE_ACCOUNT"
    CONNECT_CLIENT = "CONNECT_CLIENT"
    DISCONNECT_CLIENT = "DISCONNECT_CLIENT"
    SET_PASSWORD = "SET_PASSWORD"

# TODO: can be made cleaner by deriving message_type from function name, but then
#       that creates the restriction of function names MUST BE types, which may
#       fall flat in the future. not sure what the best option is :)
def validate_payload(message_type, required_fields):
    def decorator(func):
        async def wrapper(self, data, *args, **kwargs):
            if not self._validate_payload(data, required_fields):
                await self.send_error_response(
                    message_type,
                    f"Invalid payload data"
                )
                return
            return await func(self, data, *args, **kwargs)
        return wrapper
    return decorator

def require_privilege(message_type, required_privilege):
    def decorator(func):
        async def wrapper(self, data, *args, **kwargs):
            phone = data.get('phone')

            client = self.get_client(phone)
            if not client:
                return await self.send_error_response(message_type,
                                                      f"No client found with phone number {phone}")

            privileges = await self.get_privs(phone)
            if required_privilege not in privileges:
                await self.send_error_response(
                    message_type,
                    f"\"{required_privilege}\" missing for {phone}"
                )
                return
            return await func(self, data, client, *args, **kwargs)
        return wrapper
    return decorator


class Websocket:
    def __init__(self):
        self.webapp = get_webapp()

    @staticmethod
    async def send(typ: MessageSendType, data):
        await websocket.send(json.dumps({
            'type': typ,
            'data': data
        }))

    async def send_clients(self):
        items = [y for y in [await tg_client_blob(self.webapp, x) for x in self.webapp.client_manager.clients] if
                 y is not None]
        await self.send(MessageSendType.CLIENT_START, {
            'environment': self.webapp.execution_environment.name,
            'items': items,
        })

    async def send_error_response(self, typ, error):
        await self.send(typ, {
            'status': "ERROR",
            'error': error,
        })

    async def send_ok_response(self, typ):
        await self.send(typ, {
            'status': "OK",
            'error': None,
        })

    def get_client(self, phone):
        return next((client for client in self.webapp.client_manager.clients if client.auth.phone == phone), None)

    async def get_privs(self, phone):
        return await self.webapp.privilegesFor(request, await self.webapp.get_tg_account(phone))

    @staticmethod
    def _validate_payload(payload, keys: list[str]):
        return all(key in payload for key in keys)

    async def add_test_account(self):
        if self.webapp.execution_environment != Environment.Staging:
            return await self.send_error_response(
                MessageSendType.ADD_TEST_ACCOUNT_RESPONSE,
                "This route is only valid in a staging environment."
            )

        phone = TelegramStaging.generate_phone()
        email = ''
        comment = ''

        result = await self.webapp.account_manager.add_account(phone, email, comment, True)

        if result.success:
            await self.webapp.client_manager.add_client(self.webapp.clientFor(phone))
            print(f"added account successfully ({phone})")
            await self.send_ok_response(MessageSendType.ADD_TEST_ACCOUNT_RESPONSE)
        else:
            print(f"failed to add account: {result.error_message}")
            await self.send_error_response(MessageSendType.ADD_TEST_ACCOUNT_RESPONSE, result.error_message)

    @validate_payload(MessageSendType.SUBMIT_VALUE_RESPONSE, ['phone', 'stage', 'value'])
    @require_privilege(MessageSendType.SUBMIT_VALUE_RESPONSE, Privilege.LOGIN)
    async def submit_value(self, data, client):
        try:
            stage = data['stage']
            value = data['value']

            if client.auth.status.name != stage:
                return await self.send_error_response(MessageSendType.SUBMIT_VALUE_RESPONSE,
                                                      f"Client stage mismatch. Expected {client.auth.status.name}, got {stage}")

            try:
                client.auth.status.provideValue(value)
                await self.send_ok_response(MessageSendType.SUBMIT_VALUE_RESPONSE)
            except Exception as e:
                await self.send_error_response(MessageSendType.SUBMIT_VALUE_RESPONSE,
                                               f"Error providing value: {str(e)}")
        except Exception as e:
            await self.send_error_response(MessageSendType.SUBMIT_VALUE_RESPONSE, f"Unexpected error: {str(e)}")

    @validate_payload(MessageSendType.DELETE_ACCOUNT_RESPONSE, ['phone'])
    @require_privilege(MessageSendType.DELETE_ACCOUNT_RESPONSE, Privilege.REMOVE_ACCOUNT)
    async def delete_account(self, data, client):
        phone = data['phone']

        async def shutdown_and_remove():
            if client is not None and not client.is_stopped():
                if not client.is_stopping():
                    await client.stop()
                else:
                    # noinspection PyProtectedMember
                    await client._stop_future

            self.webapp.client_manager.clients.remove(client)
            result = await self.webapp.account_manager.delete_account(phone)

            if not result.success:
                sys.stderr.write(
                    f"[!] Could not delete account {phone}: {result.error_code} / {result.error_message}\n")

        await asyncio.create_task(shutdown_and_remove())
        await self.send_ok_response(MessageSendType.DELETE_ACCOUNT_RESPONSE)

    @validate_payload(MessageSendType.CONNECT_CLIENT_RESPONSE, ['phone'])
    @require_privilege(MessageSendType.CONNECT_CLIENT_RESPONSE, Privilege.MANAGE_CONNECTION_STATE)
    async def connect_client(self, data, client):
        if client.is_started():
            return await self.send_error_response(MessageSendType.CONNECT_CLIENT_RESPONSE, f"Client is already started")

        await client.start()
        await self.send_ok_response(MessageSendType.CONNECT_CLIENT_RESPONSE)

    @validate_payload(MessageSendType.DISCONNECT_CLIENT_RESPONSE, ['phone'])
    @require_privilege(MessageSendType.DISCONNECT_CLIENT_RESPONSE, Privilege.MANAGE_CONNECTION_STATE)
    async def disconnect_client(self, data, client):
        if not client.is_started():
            return await self.send_error_response(MessageSendType.DISCONNECT_CLIENT_RESPONSE, f"Client was not started")

        if client.is_stopped():
            return await self.send_error_response(MessageSendType.DISCONNECT_CLIENT_RESPONSE,
                                                  f"Client is already stopped")

        if client.is_stopping():
            return await self.send_error_response(MessageSendType.DISCONNECT_CLIENT_RESPONSE,
                                                  f"Client is already stopping")

        async def shutdown_client():
            info_module = next((x for x in client._modules if isinstance(x, UserInfo)), None)
            info = None if info_module is None else info_module.info

            await client.stop()

            self.webapp.client_manager.clients.remove(client)
            client.auth.status = ClientNotStarted()
            await self.webapp.client_manager.add_client(client,
                                                        start=False)  # clientFor(phone, None if info is None else info.db_username(), _get_account(phone)), False)

        await asyncio.create_task(shutdown_client())
        await self.send_ok_response(MessageSendType.DISCONNECT_CLIENT_RESPONSE)

    @validate_payload(MessageSendType.SET_PASSWORD_RESPONSE, ['phone', 'password'])
    @require_privilege(MessageSendType.SET_PASSWORD_RESPONSE, Privilege.EDIT_TWO_FACTOR_PASSWORD)
    async def set_password(self, data, client):
        phone = data['phone']
        password = data['password']

        res = await self.webapp.account_manager.set_two_factor_password(phone, password)

        if res.success:
            (await self.webapp.get_tg_account(phone)).two_factor_password = password

            if client.auth.scheme.secrets is not None:
                client.auth.scheme.secrets.two_factor_password = password
            else:
                client.auth.scheme.secrets = StaticSecrets(two_factor_password=password)

            await self.send_ok_response(MessageSendType.SET_PASSWORD_RESPONSE)
        else:
            sys.stderr.write("[!] failed to set password on account due to DB error: " + res.error_message + "\n")
            await self.send_error_response(MessageSendType.SET_PASSWORD_RESPONSE,
                                           "Failed to set password due to DB error, see stderr.")

    @validate_payload(MessageSendType.ADD_ACCOUNT_RESPONSE, ['phone'])
    async def add_account(self, data):
        try:
            phone_number = data['phone']
            email = data.get('email', None)
            comment = data.get('comment', None)

            if not re.match(r'^\d{11}$', phone_number):
                print("failed to add account: phone number must be 11 digits")
                return await self.send_error_response(MessageSendType.ADD_ACCOUNT_RESPONSE,
                                                      "Phone number must be exactly 11 digits")

            if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                print("failed to add account: invalid email format")
                return await self.send_error_response(MessageSendType.ADD_ACCOUNT_RESPONSE, "Invalid email format")

            if comment and (len(comment) < 1 or len(comment) > 300):
                print("failed to add account: comment must be between 1 and 300 characters")
                return await self.send_error_response(MessageSendType.ADD_ACCOUNT_RESPONSE,
                                                      "Comment must be between 1 and 300 characters")

            result = await self.webapp.account_manager.add_account(phone_number, email, comment)

            if result.success:
                await self.webapp.client_manager.add_client(self.webapp.clientFor(phone_number))
                print(f"added account successfully: {phone_number}")
                await self.send_ok_response(MessageSendType.ADD_ACCOUNT_RESPONSE)
            else:
                print(f"failed to add account: {result.error_message}")
                return await self.send_error_response(MessageSendType.ADD_ACCOUNT_RESPONSE, result.error_message)
        except Exception as e:
            print(f"failed to add account: unexpected error - {str(e)}")
            return await self.send_error_response(MessageSendType.ADD_ACCOUNT_RESPONSE, f"Unexpected error: {str(e)}")

    async def send_sso_start(self):
        if self.webapp.sso is not None:
            email = await self.webapp.sso.get_email()
            if email is not None:
                await self.send(MessageSendType.SSO_START, {
                    'email': email,
                })

    async def run(self):
        if self.webapp.client_manager.socket_needs_update():
            await self.send_clients()
            self.webapp.client_manager.update_socket()

        if self.webapp.privilege_manager.socket_needs_update():
            await self.send_clients()
            self.webapp.privilege_manager.update_socket()

        try:
            message = await asyncio.wait_for(websocket.receive(), timeout=1)
        except asyncio.TimeoutError:
            message = None

        if message is None:
            return

        try:
            msg = json.loads(message)
        except JSONDecodeError as e:
            print('Received invalid JSON message')
            return

        msg_type: MessageRecvType = msg['type']
        data = msg.get('data', None)
        match msg_type:
            case MessageRecvType.ADD_TEST_ACCOUNT:
                await self.add_test_account()
            case MessageRecvType.SUBMIT_VALUE:
                await self.submit_value(data)
            case MessageRecvType.DELETE_ACCOUNT:
                await self.delete_account(data)
            case MessageRecvType.CONNECT_CLIENT:
                await self.connect_client(data)
            case MessageRecvType.DISCONNECT_CLIENT:
                await self.disconnect_client(data)
            case MessageRecvType.SET_PASSWORD:
                await self.set_password(data)
            case MessageRecvType.ADD_ACCOUNT:
                await self.add_account(data)


@websocket_bp.websocket('/socket')
async def socket():
    ws = Websocket()
    await ws.send_clients()
    await ws.send_sso_start()

    while True:
        await ws.run()
