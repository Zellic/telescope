telegram enterprise account management

## building/updating

telescope-webui must be built manually:
- static export; `next build`, make sure `output: 
  'export',` is set in 
  `next.config.js`
- copy the contents of the `out` folder to 
  `telescope-webui-dist` in this repo

in the future we should probably automate this via 
docker and a submodule