Telescope
=========

Telescope is an enterprise account management system for Telegram accounts, created by Zellic. It allows organizations to manage multiple organization-controlled Telegram accounts with role-based access control (RBAC) and single sign-on (SSO) authentication.

Table of Contents
-------------------------------------------

* [Features](#features)
* [Requirements](#requirements)
* [Usage](#usage)
* [Configuration](#configuration)
* [Build Instructions](#build-instructions)
    * [Production setup](#production-setup)
    * [Development setup](#development-setup)
	* [Updating the web UI](#updating-the-web-ui)
* [Role\-Based Access Control (RBAC)](#role-based-access-control-rbac)
    * [Database schema](#database-schema)
    * [Example](#example)
    * [Privileges](#privileges)
* [Telegram Policies](#telegram-policies)
* [Development Using the Telegram Test Server](#development-using-the-telegram-test-server)
* [Pluggable Module System](#pluggable-module-system)
* [Disclaimer](#disclaimer)
* [License](#license)

Features
-------------------------------------------

* **Role-Based Access Control**: Assign privileges based on SSO email.
* **Contact Management**: Stores all one-on-one contacts found on an account in Postgres.
* **Employee Account Takeover**: Allows privileged users to retrieve two-factor codes to log into accounts. Stores 2FA passwords encrypted with a master key on disk.
* **Pluggable Module System**: Extend functionality by adding custom modules.

Requirements
-------------------------------------------
* PostgreSQL
* Docker
* Telegram API tokens (see [here](https://my.telegram.org))
* Cloudflare Access (PRs welcome for other providers.)

Usage
-------------------------------------------

Telegram accounts may be added using the "Add Account" button on the main route (`/`), or added through the self-serve onboarding interface at `/onboarding`.

When you add a new account, Telescope will proceed through the authentication steps one-by-one. If it requires more information, like an authentication code or two-factor password, the stage indicator will turn red, and the 'Provide' button will become available. Simply click that button and provide the required information so authentication can continue.

Currently, not completing authentication in a timely manner will cause the Telegram authentication code to expire. As authenticating too often is prohibited by Telegram, Telescope will not try again on its own. You must explicitly click the disconnect and reconnect buttons to begin authentication again.

The visibility of accounts, or actions related to accounts, is determined by the [RBAC system](#role-based-access-control-rbac) privileges.

Configuration
-------------------------------------------
Set the following environment variables in a `.env` file, which will be loaded by Docker Compose, or read from the project root if run without a container.

They may also be defined as environment variables by your shell.

* `HOST` The hostname to listen on (defaults to `localhost`).
* `PORT` The port to listen on (defaults to `8888`).
* `CORS_POLICY` The allowed origins for interacting with the websocket (e.g., `"https://example.com;https://example2.com"`)
* `API_ID` Your Telegram API ID from your [Telegram app](https://my.telegram.org).
* `API_HASH` Your Telegram API hash from your [Telegram app](https://my.telegram.org).
* `DB_DSN` Database connection string (e.g., `user=postgres dbname=your_dbname host=your_postgres_ip password=your_password`).
* `TWO_FACTOR_ENCRYPTION_KEY` A 32-character encryption key.
* `SSO_MODE` Authentication mode. Options are:
    * `cloudflare` For Cloudflare Access.
    * `mock` For development only; hardcodes email to `test@test.com`.
    * `disable` Skips privileges altogether, as if every user had administrator privileges.
* `CLOUDFLARE_ACCESS_CERTS` Your Cloudflare Access team subdomain (see [Cloudflare documentation](https://developers.cloudflare.com/cloudflare-one/faq/getting-started-faq)).
* `CLOUDFLARE_POLICY_AUD` Your Cloudflare Access `AUD` tag (see [Cloudflare documentation](https://developers.cloudflare.com/cloudflare-one/identity/authorization-cookie/validating-json/#get-your-aud-tag)).

Example config (all keys are correctly sized random strings for demonstration purposes):

```
API_ID=12345678
API_HASH=bce79c00b935bc325432991f88a19f0d
DB_DSN="user=postgres dbname=telescope_prod host=192.168.1.1 password=CorrectHorseBatteryStaple"
TWO_FACTOR_ENCRYPTION_KEY="dEMHhIw2jscdbKDq4orzevzlt7i7B3Rt"
CLOUDFLARE_ACCESS_CERTS="https://yourteam.cloudflareaccess.com/cdn-cgi/access/certs"
CLOUDFLARE_POLICY_AUD="e490adb9f86599ae40e26783d31e878ac69b85ab04ab04c67a0608f25181e872"
SSO_MODE="cloudflare"
```

Build Instructions
-------------------------------------------

### Production setup

1.  **Postgres**

    Install and configure Postgres - a DSN will be required.

2.  **Build Docker image**
    
    `docker compose build`
    
3.  **Create accounts directory**
    
    This is where TDLib data will live, including Telegram session persistence. This folder must be mounted into the container via Docker Compose.

    `mkdir accounts`
    
4.  **Define environment variables**
    
    Create a `.env` file with the environment variables listed in the [Configuration](#configuration) section.
    
5.  **Start the application**
    
    `docker compose up`

5. **Grant yourself admin privileges**

   No accounts will be visible unless you have privileges on them. As the operating user, you must set yourself as an administrator (granting all privileges), or configure role-based access control (see [here](#role-based-access-control-rbac).)

   To grant administrator access visit your deployed instance once so a corresponding row in the `users` is created in the Postgres database.

   Set the `is_admin` field to `true` using your SSO email:

   ```sql
   UPDATE users SET is_admin=true WHERE email='person@yourdomain.com';
   ```

   Wait five minutes for the cache to clear, or restart Telescope.

### Development setup

1.  **Build the TDLib Python JSON library**
    
    Follow the build instructions for the TDLib Python JSON library from the [official TDLib documentation](https://tdlib.github.io/td/build.html?language=Python).
    
2.  **Copy TDLib to natives/**
    
    Copy the contents of `td/tdlib` to the following platform-specific folders:
    
    * **Windows**: `natives/windows`
    * **Linux**: `natives/linux`
    * **macOS**: `natives/darwin`
    
    The resulting paths should look like:
    
    * **Windows**: `natives/windows/tdjson.dll`
    * **Linux**: `natives/linux/lib/libtdjson.so`
    * **macOS**: `natives/darwin/lib/libtdjson.dylib`
	
3.  **Set up Python virtualenv**
    
	Remember to always activate the virtualenv before running Telescope.
	
	```bash
	virtualenv .venv
	. .venv/bin/activate
    python3 -m pip install -r requirements.txt
	```
    
4.  **Set environment variables**
    
    Define the necessary environment variables as detailed in the [Configuration](#configuration) section.

5. **Development**

    See [the development section](#development-using-the-telegram-test-server) for more details.

### Updating the web UI

Currently the web UI is not built automatically by this repository's Dockerfile. In order to update the web UI, you must build a static export of the [web UI repository](https://github.com/Zellic/telescope-webui) and copy the contents of the `out` folder to the `telescope-webui-dist` folder in this repository. PRs to improve this process are welcome.

Role-Based Access Control (RBAC)
-------------------------------------------
### Database usage
Telescope uses an RBAC system to manage user privileges, which are defined in the following Postgres tables:

1.  `roles` Maps role IDs to human readable names.

2.  `users` When you first visit the application, a row is added to the `users` table using your SSO email. This account can be set as `is_admin=true`, granting total permissions, or have one or more role IDs assigned using PostgreSQL array syntax (e.g., `{1, 2}`).
    
3.  `telegram_groups` Maps Telegram group IDs to human readable names.
    
4.  `telegram_accounts` Telegram accounts may be assigned one or more group IDs in the `group` field.
    
5.  `telegram_privileges` Assign specific privileges to roles for Telegram accounts within specific groups.
    
### Example
	
For example, to grant the `sales` role (ID: 1) privileges on the `sales` account group (ID: 1):

```sql
INSERT INTO telegram_privileges (group_id, role_id, privileges)  VALUES (1, 1, '{"view", "login", "manage_connection_state"}');
```

But the `management` role (ID: 2) may also have privileges on the `sales` account group (ID: 1):

```sql
INSERT INTO telegram_privileges (group_id, role_id, privileges)  VALUES (1, 2, '{"view", "login", "manage_connection_state", "remove_account"}');
```

### Privileges

Privileges are cached and refresh every five minutes. The current set of privileges are:

- `view`
  
  Whether this user may see this account at all.

- `edit_two_factor_password`
  
  Whether this user may edit the account's two-factor password.
  
- `login`
  
  Whether this user may retrieve the most recent authentication code for this account, allowing them to log in to Telegram with this account. (Note: There is currently no way to retrieve two-factor *passwords*, Telescope only uses them internally if provided.)

- `manage_connection_state`
  
  Whether this user may connect or disconnect Telescope's Telegram session for this account. Note that this does *not* clear the tdlib session token, so **this will not count as authenticating again**, rather, it is the same as closing and reopening your Telegram app on desktop.

- `remove_account`
  
  Whether this user may remove this account from Telegram (drop the row from the database).

Telegram Policies
-------------------------------------------
On the Telegram production servers, if you authenticate on an account more than five times in a day - whether successful or not - you will not be able to authenticate again on that account for that day.

Unusual numbers of authentications, especially failed attempts, may risk your Telegram API key being banned. Telescope does not attempt to prevent this.

Note that restarting Telescope will not cause any accounts to authenticate again. Telegram session tokens are stored by tdlib in the `accounts/` folder. Deleting that folder will cause all accounts to authenticate again.

 **Please use responsibly.**

Development Using the Telegram Test Server
-------------------------------------------
Telescope supports using the [Telegram test environment](https://core.telegram.org/api/auth#test-accounts) during development.

1.  **Database**:

    Real Telegram accounts should not try to authenticate to the test environment. Instead, configure a separate DSN for testing.

2.  **Run test entry point**:
    
    Instead of running `main.py`, use `test.py`.
    
3.  **Add test account**:
    
    Use the "Add Test Account" button in the web UI to automatically add a test account.
    
    * **Note**: You will likely not see the test account due to the default RBAC configuration lacking the VIEW privilege.
      
      It will be visible if:
	
	  - You are in `SSO_MODE=MOCK` and the Telegram account is set to `test@test.com`.
	  - You are in `SSO_MODE=MOCK` and the `test@test.com` user has `is_admin` in the `users` table set to `true`.
	  - You are in `SSO_MODE=MOCK` and you have configured RBAC privileges that would allow you to see the account.
	  - You are in `SSO_MODE=cloudflare` and use Cloudflare Access during development.
	  - You are in `SSO_MODE=disable`, so the RBAC system grants all privileges universally.

4.  **Authenticate test account**:

    Telegram test accounts have authentication codes automatically set based on their phone number. The web UI will display each account's authentication code in the leftmost column of the main page.
	
	Test accounts do *not* have two-factor passwords set by default, however, other Telegram developers may happen to use the same random phone number and set a two-factor password on it while testing. If you are prompted for a two-factor password, simply remove that account and add another one.
	
	Similarly, test accounts may have inappropriate names set by third parties during their use of the Telegram test environment. As these servers are operated by the Telegram corporation, this is outside our control.

Pluggable Module System
-------------------------------------------
Telescope features a pluggable module system that allows for extending functionality. For example, the `SaveContacts` module handles storing contacts.

Event types used in the `@OnEvent` decorator come directly from the [official TDLib API documentation](https://core.telegram.org/tdlib/docs/classtd_1_1td__api_1_1_update.html).

Note: You may set `LOG_ALL=True` at the top of `tdlib.py` to dump all TDLib JSON messages if the TDLib documentation is insufficient or unclear.

Disclaimer
-------------------------------------------
Zellic makes no warranties, express or implied, regarding this project's performance or fitness for a particular purpose. Use at your own risk. We disclaim any liability for damages arising from improper use, software malfunction, or unforeseen consequences.
