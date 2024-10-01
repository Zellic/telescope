import json
from enum import Enum
from quart import websocket, Blueprint, request
from telegram.webapp.websocket.util import tg_client_blob, get_webapp

websocket_bp = Blueprint('socket_bp', __name__)

class WebsocketType(str, Enum):
    CLIENT_START = 'CLIENT_START'

class Websocket:
    def __init__(self):
        self.webapp = get_webapp()

    @staticmethod
    async def send(typ: WebsocketType, data):
        await websocket.send(json.dumps({
            'type': typ,
            'data': data
        }))

    async def send_clients(self):
        items = [y for y in [await tg_client_blob(self.webapp, x) for x in self.webapp.client_manager.clients] if y is not None]
        await self.send(WebsocketType.CLIENT_START, {
            'hash': str(hash(json.dumps(items))),
            'environment': self.webapp.execution_environment.name,
            'items': items,
        })

    async def run(self):
        await websocket.receive()

@websocket_bp.websocket('/socket')
async def socket():
    ws = Websocket()
    await ws.send_clients()

    while True:
        await ws.run()