from typing import Optional

from quart import Request

# just a stub for now, unclear what the API should look like for other sso systems
class SSOModule:
	async def get_email(self) -> Optional[str]:
		raise NotImplementedError()