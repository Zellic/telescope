telegram enterprise account management

## Building/updating the web UI

The `telescope-webui` repository must be built manually 
and committed to this repo:
- static export: `next build`, make sure `output: 
  'export',` is set in 
  `next.config.js`
- copy the contents of the `out` folder to 
  `telescope-webui-dist` in this repo

In the future we should probably automate this via 
docker and a submodule.

## Testing
When testing during development you should use `test.py` 
instead of `main.py`, which will use the 
`TelegramStaging` authentication scheme rather than 
`TelegramProduction`. You will not be able to use real
Telegram accounts under this configuration, and you should
use a separate testing or staging database via environment
variables.

This allows for using `TelegramStaging.generate_phone()` 
- per [Telegram's API documentation](https://core.telegram.org/api/auth#test-accounts), we may make as 
  many accounts as we need to (only on the test DC), and 
  authenticating repeatedly, as well as authentication 
  failures, will not penalize our app ID.

For testing purposes it is possible to add accounts to 
the manager directly, but for a production-like 
environment test accounts should be generated with 
`generate_phone` and added to the database via SQL query.
Unfortunately, in production we use eleven digit phone 
numbers and the web UI is designed with that in mind, 
but the test DC *requires* 10 digit phone numbers. Thus, 
you cannot add a test account to the database via the 
Add Account modal in the web UI.

Keep in mind the auth code can be 
derived from the phone number, and `TelegramStaging` 
will print the appropriate log-in code at initialization 
time for each account.