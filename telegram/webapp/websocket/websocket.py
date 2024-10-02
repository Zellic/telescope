import json
from enum import Enum
from json import JSONDecodeError

from quart import websocket, Blueprint, request

from database.accesscontrol import Privilege
from telegram.auth.schemes.staging import TelegramStaging
from telegram.util import Environment
from telegram.webapp.websocket.util import tg_client_blob, get_webapp

websocket_bp = Blueprint('socket_bp', __name__)


class MessageSendType(str, Enum):
    CLIENT_START = 'CLIENT_START'
    ADD_TEST_ACCOUNT_RESPONSE = "ADD_TEST_ACCOUNT_RESPONSE"
    SUBMIT_VALUE_RESPONSE = "SUBMIT_VALUE_RESPONSE"


class MessageRecvType(str, Enum):
    ADD_TEST_ACCOUNT = 'ADD_TEST_ACCOUNT'
    SUBMIT_VALUE = 'SUBMIT_VALUE'


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
            await self.send_clients()
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
                await self.send_clients()
                await self.send_ok_response(MessageSendType.SUBMIT_VALUE_RESPONSE)
            except Exception as e:
                await self.send_error_response(MessageSendType.SUBMIT_VALUE_RESPONSE,
                                               f"Error providing value: {str(e)}")
        except Exception as e:
            await self.send_error_response(MessageSendType.SUBMIT_VALUE_RESPONSE, f"Unexpected error: {str(e)}")

    async def run(self):
        message = await websocket.receive()
        print(message)
        if message is None:
            return

        try:
            msg = json.loads(message)
        except JSONDecodeError as e:
            print('Received invalid JSON message')
            return

        match msg['type']:
            case MessageRecvType.SUBMIT_VALUE:
                await self.submit_value(msg['data'])
            case MessageRecvType.ADD_TEST_ACCOUNT:
                await self.add_test_account()


@websocket_bp.websocket('/socket')
async def socket():
    ws = Websocket()
    await ws.send_clients()

    while True:
        await ws.run()
