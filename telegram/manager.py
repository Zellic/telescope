from typing import Dict, List

from telegram.client import TelegramClient


class TelegramClientManager:
    def __init__(self):
        self.clients: List[TelegramClient] = []

    def add_client(self, client: TelegramClient):
        self.clients.append(client)
        client.start()

    # TODO: some way to call .stop() on the client have it bubble up and remove it from this list
    # or alternatively you call stop on the manager with some client id?