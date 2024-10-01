import os

from quart import Quart, send_from_directory, abort, Request
from quart_cors import cors

from database.accesscontrol import UserPrivilegeManager, Privilege
from database.accounts import AccountManager, TelegramAccount
from sso.cloudflare import CloudflareAccessSSO
from sso.mock import MockSSO
from sso.ssomodule import SSOModule
from telegram.manager import TelegramClientManager
from telegram.util import Environment
from telegram.webapp.websocket.websocket import websocket_bp

ALLOWED_EXTENSIONS = {'html', 'js', 'css', 'png', 'jpg', 'gif', 'ico', 'svg'}
_ALL_PRIVILEGES = set(x for x in Privilege)

class WebApp:
    app: Quart
    frontend_path: str
    clientFor: any
    execution_environment: Environment
    account_manager: AccountManager
    client_manager: TelegramClientManager
    privilege_manager: UserPrivilegeManager
    sso: SSOModule | None
    account_cache: dict

    def __init__(self,
                 config: dict,
                 manager: TelegramClientManager,
                 accounts: AccountManager,
                 clientFor: any,
                 environment: Environment,
                 privmanager: UserPrivilegeManager):
        self.clientFor = clientFor
        self.execution_environment = environment
        self.account_manager = accounts
        self.client_manager = manager
        self.privilege_manager = privmanager
        self.frontend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", 'telescope-webui-dist')
        self.account_cache = {}

        _app = Quart(__name__)
        self.app = cors(_app, allow_origin="http://localhost:3000")
        self.app.config['webapp'] = self

        self.setup_sso(config)
        self.setup_routes()

    def setup_routes(self):
        self.app.register_blueprint(websocket_bp)

        @self.app.route('/<path:asset_path>')
        async def serve_static(asset_path):
            path = os.path.join(self.frontend_path, asset_path)
            if not self.is_allowed_file(path, self.frontend_path):
                abort(404)
            try_paths = [path, path + ".html", path + ".htm"]
            for path in try_paths:
                if os.path.isfile(path):
                    directory, file = os.path.split(path)
                    return await send_from_directory(directory, file)
            abort(404)

        @self.app.route('/', defaults={'path': ''})
        @self.app.route('/<path:path>')
        async def serve_index(path):
            return await send_from_directory(self.frontend_path, 'index.html')

    def setup_sso(self, config):
        self.sso = None

        mode = config.get("SSO_MODE", "cloudflare").lower()

        if mode == "mock":
            if self.execution_environment != Environment.Staging:
                raise NotImplementedError("Cannot use SSO_MODE=mock outside staging environment")

            # hardcode user to email test@test.com
            self.sso = MockSSO()
        elif mode == "disable":
            self.sso = None
        elif mode == "cloudflare":
            try:
                self.sso = CloudflareAccessSSO(config["CLOUDFLARE_ACCESS_CERTS"], config["CLOUDFLARE_POLICY_AUD"])
            except KeyError:
                raise Exception("Missing SSO config options... (CLOUDFLARE_ACCESS_CERTS, CLOUDFLARE_POLICY_AUD)")
        else:
            raise NotImplementedError("Unknown/unhandled SSO mode: " + mode)

    async def get_tg_account(self, phone: str) -> TelegramAccount:
        if phone in self.account_cache:
            account = self.account_cache[phone]
        else:
            account = await self.account_manager.get_account(phone)

        self.account_cache[phone] = account
        return account

    async def privilegesFor(self, req: Request, account: TelegramAccount) -> set[Privilege]:
        """retrieve the set of privileges this user (as determined by their cloudflare SSO email) has on this TG account"""

        if self.sso is None:
            if self.execution_environment != Environment.Staging:
                raise NotImplementedError()

            # while debugging, simply show all accounts
            return _ALL_PRIVILEGES

        email = await self.sso.get_email(req)
        if email is None:
            return set()

        user = await self.privilege_manager.get_or_create_user(email)

        if user.is_admin:
            return _ALL_PRIVILEGES

        privs = await self.privilege_manager.get_privileges_on_account(user, account)
        return privs

    @staticmethod
    def is_allowed_file(path, root):
        try:
            real_path = os.path.realpath(path)
            real_root = os.path.realpath(root)

            common_prefix = os.path.commonpath([real_path, real_root])

            return common_prefix == real_root
        except ValueError:
            return False
        except OSError:
            return False