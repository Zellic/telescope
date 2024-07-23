import asyncio
from typing import Dict, List, AsyncIterator

from telegram.client import TelegramClient
from telegram.tdlib import TDLib


class TelegramClientManager:
    def __init__(self):
        self.clients: List[TelegramClient] = []
        self.tdlib = TDLib()
        # set log level to error
        self.tdlib.td_execute({'@type': 'setLogVerbosityLevel', 'new_verbosity_level': 1})

        self._extra_counter = 0
        self._pending_responses = {}
        self._lock = asyncio.Lock()
        self._stop_event = asyncio.Event()
        self._task = None
        self._started = False

    def add_client(self, client: TelegramClient):
        self.clients.append(client)
        # gross hack, difficult to conveniently fix without splitting this into two classes
        # let's just not!
        client._tdlib = self.tdlib

        if(self._started):
            client.start()

    def _try_dispatch_event(self):
        event = self.tdlib.receive()

        if(event is None):
            return False

        client_id = event['@client_id']
        client = next((x for x in self.clients if x.client_id == client_id), None)

        if(client is None):
            print(f"[!] Unhandled message for client ID: {client_id}")
            return True

        # noinspection PyProtectedMember
        client._event_received(event)
        return True

    async def _receive_loop(self):
        c = 0
        while not self._stop_event.is_set():
            c += 1
            if(c > 100 or not self._try_dispatch_event()):
                c = 0
                await asyncio.sleep(1.0)
            else:
                await asyncio.sleep(0.01)
        print('exit receive loop')

    def is_started(self):
        return self._started

    def start(self):
        if (self.is_started()):
            raise Exception("Already started")

        for client in self.clients:
            client.start()

        self._started = True
        self._task = asyncio.get_event_loop().create_task(self._receive_loop())
        return self._task

    # TODO: there is no method to stop a single client and stop listening to it
    async def stop_and_yield(self) -> AsyncIterator[TelegramClient]:
        if not self.is_started():
            raise Exception("Hasn't been started yet")

        async def inner(client):
            await client.stop()
            return client

        print(f"Halting {len(self.clients)} clients...")
        for client in asyncio.as_completed([inner(client) for client in self.clients]):
            yield await client

        self._stop_event.set()
        await self._task

    async def stop(self):
        if (not self.is_started()):
            raise Exception("Hasn't been started yet")

        async for _ in self.stop_and_yield():
            pass