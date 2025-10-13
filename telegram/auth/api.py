import json
import asyncio
import time
from typing import Callable, List, Optional

from telegram.auth.base import AuthenticationProvider, APIAuthState, AuthenticationScheme
from telegram.client import TelegramClient

# Phone code timeout duration in seconds (can be changed for debugging)
PHONE_CODE_TIMEOUT_SECONDS = 5  # 20 minutes

"""
This is the default state when we haven't started a connection to the server yet
"""
class ClientNotStarted(APIAuthState):
	name = "ClientNotStarted"
	requiresInput = False

"""
This is the default post-connect state when the server hasn't asked us for anything yet.
"""
class WaitingOnServer(APIAuthState):
	name = "WaitingOnServer"
	requiresInput = False

class PasswordRequired(APIAuthState):
	name = "PasswordRequired"
	requiresInput = True

class AuthCodeRequired(APIAuthState):
	name = "AuthCodeRequired"
	requiresInput = True

class RegistrationRequired(APIAuthState):
	name = "RegistrationRequired"
	requiresInput = False

class PhoneNumberRequired(APIAuthState):
	name = "PhoneNumberRequired"
	requiresInput = False

class EmailRequired(APIAuthState):
	name = "EmailRequired"
	requiresInput = True

class EmailCodeRequired(APIAuthState):
	name = "EmailCodeRequired"
	requiresInput = True

class AuthorizationSuccess(APIAuthState):
	name = "AuthorizationSuccess"
	requiresInput = False

class ConnectionClosed(APIAuthState):
	name = "ConnectionClosed"
	requiresInput = False

class ErrorOccurred(APIAuthState):
	name = "ErrorOccurred"
	requiresInput = False

	def __init__(self, error):
		super().__init__()
		self.error = error

class APIEvent:
	def to_json(self) -> str:
		return json.dumps(self.__dict__)

class NewAuthenticationStage(APIEvent):
	def __init__(self, stage: str):
		self.type = "NewAuthenticationState"
		self.state = stage

class InputReceived(APIEvent):
	def __init__(self, stage: str, value: str):
		self.type = "InputReceived"
		self.input_type = stage
		self.value = value

class APIAuth(AuthenticationProvider):
	def __init__(self, phone: str, scheme: AuthenticationScheme, account_manager=None):
		self.phone = phone
		self.scheme: AuthenticationScheme = scheme
		self._status: APIAuthState = ClientNotStarted()
		self._event_callbacks: List[Callable[[APIEvent], None]] = []
		self._account_manager = account_manager
		self._phone_code_timeout_task: Optional[asyncio.Task] = None
		self._phone_code_request_time: Optional[float] = None

	@property
	def status(self):
		return self._status

	@status.setter
	def status(self, value):
		self._status = value
		self._notify_event(NewAuthenticationStage(type(value).__name__))

	def add_event_callback(self, callback: Callable[[APIEvent], None]):
		self._event_callbacks.append(callback)

	def _notify_event(self, event: APIEvent):
		for callback in self._event_callbacks:
			callback(event)

	def _start_phone_code_timeout(self, client: TelegramClient):
		"""Start a 20-minute timeout for phone code expiration"""
		if self._phone_code_timeout_task and not self._phone_code_timeout_task.done():
			self._phone_code_timeout_task.cancel()
		
		self._phone_code_request_time = time.time()
		
		# Store the timeout info in the database for persistence
		if self._account_manager:
			asyncio.create_task(self._account_manager.set_phone_code_timeout(self.phone, self._phone_code_request_time))
		
		async def timeout_handler():
			await asyncio.sleep(PHONE_CODE_TIMEOUT_SECONDS)  # Phone code timeout
			# If we reach here, the phone code has expired
			print(f"Phone code timeout expired for {self.phone} - disconnecting client")
			# Clear the timeout from database
			if self._account_manager:
				await self._account_manager.clear_phone_code_timeout(self.phone)
			# Disconnect the client to force reconnection
			# This puts the client back to disconnected state
			if hasattr(client, 'stop'):
				await client.stop()
				print(f"Client disconnected for {self.phone} due to phone code timeout")

		self._phone_code_timeout_task = asyncio.create_task(timeout_handler())

	def _cancel_phone_code_timeout(self):
		"""Cancel the phone code timeout when code is provided"""
		if self._phone_code_timeout_task and not self._phone_code_timeout_task.done():
			self._phone_code_timeout_task.cancel()
		self._phone_code_timeout_task = None
		self._phone_code_request_time = None
		# Clear the timeout from database
		if self._account_manager:
			asyncio.create_task(self._account_manager.clear_phone_code_timeout(self.phone))

	async def check_phone_code_expiration(self, client: TelegramClient):
		"""Check if phone code has expired based on stored timeout info"""
		if self._account_manager:
			request_time = await self._account_manager.get_phone_code_timeout(self.phone)
			if request_time:
				elapsed_time = time.time() - request_time
				if elapsed_time >= PHONE_CODE_TIMEOUT_SECONDS:  # Phone code timeout
					print(f"Phone code timeout expired for {self.phone} on startup - disconnecting client")
					# Clean up the stored timeout info
					await self._account_manager.clear_phone_code_timeout(self.phone)
					# Disconnect the client to force reconnection
					# This puts the client back to disconnected state
					if hasattr(client, 'stop'):
						await client.stop()
						print(f"Client disconnected for {self.phone} due to expired phone code timeout")
					return True
				else:
					# Still within timeout, restart the remaining time
					remaining_time = PHONE_CODE_TIMEOUT_SECONDS - elapsed_time
					self._phone_code_request_time = request_time
					self._restart_phone_code_timeout(client, remaining_time)
		return False

	def _restart_phone_code_timeout(self, client: TelegramClient, remaining_time: float):
		"""Restart phone code timeout with remaining time"""
		if self._phone_code_timeout_task and not self._phone_code_timeout_task.done():
			self._phone_code_timeout_task.cancel()
		
		async def timeout_handler():
			await asyncio.sleep(remaining_time)
			# If we reach here, the phone code has expired
			print(f"Phone code timeout expired for {self.phone} (restarted) - disconnecting client")
			# Clear the timeout from database
			if self._account_manager:
				await self._account_manager.clear_phone_code_timeout(self.phone)
			# Disconnect the client to force reconnection
			# This puts the client back to disconnected state
			if hasattr(client, 'stop'):
				await client.stop()
				print(f"Client disconnected for {self.phone} due to phone code timeout (restarted)")

		self._phone_code_timeout_task = asyncio.create_task(timeout_handler())


	def authorizationStateWaitTdlibParameters(self, client: TelegramClient):
		self.scheme.authorizationStateWaitTdlibParameters(client)
		self.status = WaitingOnServer()

	def authorizationStateReady(self, client: TelegramClient):
		self.scheme.authorizationStateReady(client)
		# Cancel any pending phone code timeout on successful auth
		self._cancel_phone_code_timeout()
		self.status = AuthorizationSuccess()

	# TODO: implement authorizationStateClosing as well

	def authorizationStateClosed(self, client: TelegramClient):
		self.scheme.authorizationStateClosed(client)
		# Cancel any pending phone code timeout
		self._cancel_phone_code_timeout()
		# TODO: this should be connection closed, not auth failed
		self.status = ConnectionClosed()

	def authorizationStateWaitPhoneNumber(self, client: TelegramClient):
		self.scheme.authorizationStateWaitPhoneNumber(client, self.phone)
		self.status = PhoneNumberRequired()

	def authorizationStateWaitEmailAddress(self, client: TelegramClient):
		self.status = EmailRequired()

		def wait(value):
			self.scheme.authorizationStateWaitEmailAddress(client, value)
			self._notify_event(InputReceived(self.status.name, value))

		self.status.waitForValue(wait)

	def authorizationStateWaitPassword(self, client: TelegramClient):
		if(self.scheme.secrets is not None and self.scheme.secrets.two_factor_password is not None):
			staticpass = self.scheme.secrets.two_factor_password
			self.status = PasswordRequired()
			self.scheme.authorizationStateWaitPassword(client, staticpass)
			self._notify_event(InputReceived(self.status.name, staticpass))
			return

		self.status = PasswordRequired()

		def wait(value):
			self.scheme.authorizationStateWaitPassword(client, value)
			self._notify_event(InputReceived(self.status.name, value))

		self.status.waitForValue(wait)

	def authorizationStateWaitEmailCode(self, client: TelegramClient):
		self.status = EmailCodeRequired()

		def wait(value):
			self.scheme.authorizationStateWaitEmailCode(client, value)
			self._notify_event(InputReceived(self.status.name, value))

		self.status.waitForValue(wait)

	def authorizationStateWaitCode(self, client: TelegramClient):
		self.status = AuthCodeRequired()
		# Start the 20-minute timeout for phone code expiration
		self._start_phone_code_timeout(client)

		def wait(value):
			# Cancel timeout when code is provided
			self._cancel_phone_code_timeout()
			self.scheme.authorizationStateWaitCode(client, value)
			self._notify_event(InputReceived(self.status.name, value))

		self.status.waitForValue(wait)

	# only implemented for development, not used in production
	def authorizationStateWaitRegistration(self, client: 'TelegramClient'):
		self.status = RegistrationRequired()
		self.scheme.authorizationStateWaitRegistration(client, None)