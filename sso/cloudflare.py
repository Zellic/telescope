import json
import time
from typing import Optional

import jwt
import requests
from quart import Request, websocket

from sso.ssomodule import SSOModule

class CloudflareJWT:
    CACHE_DURATION_IN_SECONDS = 3600

    def __init__(self, certs_url, policy_aud):
        self.certs_url = certs_url
        self.policy_aud = policy_aud
        self._public_keys = None
        self._last_fetched = None

    def _get_public_keys(self):
        current_time = time.monotonic()
        if self._public_keys is None or current_time - self._last_fetched > self.CACHE_DURATION_IN_SECONDS:
            # TODO: do this asynchronously
            r = requests.get(self.certs_url)
            jwk_set = r.json()
            # noinspection PyUnresolvedReferences
            self._public_keys = [
                jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key_dict))
                for key_dict in jwk_set['keys']
            ]
            self._last_fetched = current_time
        return self._public_keys

    def verify_token(self, authorization_header) -> Optional[str]:
        if not authorization_header:
            return None

        keys = self._get_public_keys()

        for key in keys:
            try:
                return jwt.decode(authorization_header, key=key, audience=self.policy_aud, algorithms=['RS256'])['email']
            except jwt.InvalidTokenError:
                continue

        return None

class CloudflareAccessSSO(SSOModule):
    def __init__(self, certs_url, policy_aud):
        self.cjwt = CloudflareJWT(certs_url, policy_aud)

    async def get_email(self) -> Optional[str]:
        auth = websocket.cookies.get("CF_Authorization")
        if auth is None:
            return None

        return self.cjwt.verify_token(auth)