from typing import Optional

from quart import Request

from sso.ssomodule import SSOModule

class MockSSO(SSOModule):
    async def get_email(self) -> Optional[str]:
        return "test@test.com"