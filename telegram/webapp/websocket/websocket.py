import asyncio
import json
import re
import sys
from enum import Enum
from json import JSONDecodeError

from quart import websocket, Blueprint, request

from database.accesscontrol import Privilege
from telegram.auth.api import ClientNotStarted
from telegram.auth.base import StaticSecrets
from telegram.auth.schemes.staging import TelegramStaging
from telegram.tgmodules.userinfo import UserInfo
from telegram.util import Environment
from telegram.webapp.websocket.util import tg_client_blob, get_webapp

websocket_bp = Blueprint('socket_bp', __name__)

class MessageSendType(str, Enum):
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

    async def add_test_account(self):
        if self.webapp.execution_environment != Environment.Staging:
            await self.send_error_response(
                MessageSendType.ADD_TEST_ACCOUNT_RESPONSE,
                "This route is only valid in a staging environment."
            )
            return

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

    async def submit_value(self, data):
        try:
            if not all(key in data for key in ['phone', 'stage', 'value']):
                await self.send_error_response(MessageSendType.SUBMIT_VALUE_RESPONSE, "Invalid payload structure")
                return

            phone = data['phone']
            stage = data['stage']
            value = data['value']

            matching_client = next(
                (client for client in self.webapp.client_manager.clients if client.auth.phone == phone), None)

            if not matching_client:
                await self.send_error_response(MessageSendType.SUBMIT_VALUE_RESPONSE,
                                               f"No client found with phone number {phone}")
                return

            privileges = await self.webapp.privilegesFor(request, await self.webapp.get_tg_account(phone))

            if Privilege.LOGIN not in privileges:
                await self.send_error_response(MessageSendType.SUBMIT_VALUE_RESPONSE,
                                               f"Insufficient privileges to provide for {phone}")
                return

            if matching_client.auth.status.name != stage:
                await self.send_error_response(MessageSendType.SUBMIT_VALUE_RESPONSE,
                                               f"Client stage mismatch. Expected {matching_client.auth.status.name}, got {stage}")
                return

            try:
                matching_client.auth.status.provideValue(value)
                await self.send_ok_response(MessageSendType.SUBMIT_VALUE_RESPONSE)
            except Exception as e:
                await self.send_error_response(MessageSendType.SUBMIT_VALUE_RESPONSE,
                                               f"Error providing value: {str(e)}")
        except Exception as e:
            await self.send_error_response(MessageSendType.SUBMIT_VALUE_RESPONSE, f"Unexpected error: {str(e)}")

    async def delete_account(self, data):
        if not 'phone' in data:
            await self.send_error_response(MessageSendType.DELETE_ACCOUNT_RESPONSE, "Invalid payload structure")
            return

        phone = data['phone']

        client = next((x for x in self.webapp.client_manager.clients if x.auth.phone == phone), None)

        if client is None:
            await self.send_error_response(MessageSendType.DELETE_ACCOUNT_RESPONSE,
                                           f"Couldn't find client with phone number: {phone}")
            return

        privileges = await self.webapp.privilegesFor(request, await self.webapp.get_tg_account(phone))

        if Privilege.REMOVE_ACCOUNT not in privileges:
            await self.send_error_response(MessageSendType.DELETE_ACCOUNT_RESPONSE,
                                           f"Insufficient privileges to delete account {phone}")
            return

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

    async def connect_client(self, data):
        if not 'phone' in data:
            await self.send_error_response(MessageSendType.CONNECT_CLIENT_RESPONSE, "Invalid payload structure")
            return

        phone = data['phone']

        client = next((x for x in self.webapp.client_manager.clients if x.auth.phone == phone), None)

        if client is None:
            await self.send_error_response(MessageSendType.CONNECT_CLIENT_RESPONSE,
                                           f"Couldn't find client with phone number: {phone}")
            return

        privileges = await self.webapp.privilegesFor(request, await self.webapp.get_tg_account(phone))

        if Privilege.MANAGE_CONNECTION_STATE not in privileges:
            await self.send_error_response(MessageSendType.CONNECT_CLIENT_RESPONSE,
                                           f"Insufficient privileges to manage connection state for {phone}")
            return

        if client.is_started():
            await self.send_error_response(MessageSendType.CONNECT_CLIENT_RESPONSE, f"Client is already started")
            return

        await client.start()
        await self.send_ok_response(MessageSendType.CONNECT_CLIENT_RESPONSE)

    async def disconnect_client(self, data):
        if not 'phone' in data:
            await self.send_error_response(MessageSendType.DISCONNECT_CLIENT_RESPONSE, "Invalid payload structure")
            return

        phone = data['phone']

        client = next((x for x in self.webapp.client_manager.clients if x.auth.phone == phone), None)

        if client is None:
            await self.send_error_response(MessageSendType.DISCONNECT_CLIENT_RESPONSE,
                                           f"Couldn't find client with phone number: {phone}")
            return

        privileges = await self.webapp.privilegesFor(request, await self.webapp.get_tg_account(phone))

        if Privilege.MANAGE_CONNECTION_STATE not in privileges:
            await self.send_error_response(MessageSendType.DISCONNECT_CLIENT_RESPONSE,
                                           f"Insufficient privileges to manage connection state for {phone}")
            return

        if not client.is_started():
            await self.send_error_response(MessageSendType.DISCONNECT_CLIENT_RESPONSE, f"Client was not started")
            return

        if client.is_stopped():
            await self.send_error_response(MessageSendType.DISCONNECT_CLIENT_RESPONSE, f"Client is already stopped")
            return

        if client.is_stopping():
            await self.send_error_response(MessageSendType.DISCONNECT_CLIENT_RESPONSE, f"Client is already stopping")
            return

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

    async def set_password(self, data):
        if not all(key in data for key in ['password', 'phone']):
            await self.send_error_response(MessageSendType.SET_PASSWORD_RESPONSE, "Invalid payload structure")
            return

        phone = data['phone']
        password = data['password']

        client = next((x for x in self.webapp.client_manager.clients if x.auth.phone == phone), None)

        if client is None:
            await self.send_error_response(MessageSendType.SET_PASSWORD_RESPONSE,
                                           f"Couldn't find client with phone number: {phone}")
            return

        privileges = await self.webapp.privilegesFor(request, await self.webapp.get_tg_account(phone))

        if Privilege.EDIT_TWO_FACTOR_PASSWORD not in privileges:
            await self.send_error_response(MessageSendType.SET_PASSWORD_RESPONSE,
                                           f"Insufficient privileges to set two factor password for {phone}")
            return

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

    async def add_account(self, data):
        try:
            if not 'phone' in data:
                await self.send_error_response(MessageSendType.ADD_ACCOUNT_RESPONSE, "Invalid payload structure")
                return

            phone_number = data['phone']
            email = data.get('email', None)
            comment = data.get('comment', None)

            if not re.match(r'^\d{11}$', phone_number):
                print("failed to add account: phone number must be 11 digits")
                await self.send_error_response(MessageSendType.ADD_ACCOUNT_RESPONSE, "Phone number must be exactly 11 digits")
                return

            if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                print("failed to add account: invalid email format")
                await self.send_error_response(MessageSendType.ADD_ACCOUNT_RESPONSE, "Invalid email format")
                return

            if comment and (len(comment) < 1 or len(comment) > 300):
                print("failed to add account: comment must be between 1 and 300 characters")
                await self.send_error_response(MessageSendType.ADD_ACCOUNT_RESPONSE, "Comment must be between 1 and 300 characters")
                return

            result = await self.webapp.account_manager.add_account(phone_number, email, comment)

            if result.success:
                await self.webapp.client_manager.add_client(self.webapp.clientFor(phone_number))
                print(f"added account successfully: {phone_number}")
                await self.send_ok_response(MessageSendType.ADD_ACCOUNT_RESPONSE)
            else:
                print(f"failed to add account: {result.error_message}")
                await self.send_error_response(MessageSendType.ADD_ACCOUNT_RESPONSE, result.error_message)
                return
        except Exception as e:
            print(f"failed to add account: unexpected error - {str(e)}")
            return json.dumps({"error": f"Unexpected error: {str(e)}"}), 500

    async def run(self):
        if self.webapp.client_manager.socket_needs_update():
            await self.send_clients()
            self.webapp.client_manager.update_socket()

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
        match msg_type:
            case MessageRecvType.SUBMIT_VALUE:
                data = msg['data']
                await self.submit_value(data)
            case MessageRecvType.ADD_TEST_ACCOUNT:
                await self.add_test_account()
            case MessageRecvType.DELETE_ACCOUNT:
                data = msg['data']
                await self.delete_account(data)
            case MessageRecvType.CONNECT_CLIENT:
                data = msg['data']
                await self.connect_client(data)
            case MessageRecvType.DISCONNECT_CLIENT:
                data = msg['data']
                await self.disconnect_client(data)
            case MessageRecvType.SET_PASSWORD:
                data = msg['data']
                await self.set_password(data)
            case MessageRecvType.ADD_ACCOUNT:
                data = msg['data']
                await self.add_account(data)


@websocket_bp.websocket('/socket')
async def socket():
    ws = Websocket()
    await ws.send_clients()

    while True:
        await ws.run()
