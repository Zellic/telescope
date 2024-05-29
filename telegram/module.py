import functools
from typing import Callable, Awaitable, NoReturn

TelegramEventHandler = Callable[['TelegramClient', str], Awaitable[NoReturn]]


# noinspection PyShadowingBuiltins
def OnEvent(type: str):
	def decorator(func: TelegramEventHandler):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			return func(*args, **kwargs)
		wrapper.type = type
		return wrapper
	return decorator

class TelegramModule:
	def onClientExit(self):
		pass