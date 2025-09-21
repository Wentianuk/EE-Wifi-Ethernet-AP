# OpenWrt Packaging Notes

## Repository Layout
- `package/ee-wifi-autologin/Makefile`: OpenWrt package definition.
- `package/ee-wifi-autologin/files/usr/share/ee-wifi-autologin/ee_wifi_autologin.py`: Lightweight Python agent.
- `package/ee-wifi-autologin/files/etc/init.d/ee-wifi-autologin`: `procd` init script.
- `package/ee-wifi-autologin/files/etc/ee-wifi-autologin.json.example`: Config template.
- `PORTING_PLAN.md`: High-level porting strategy and outstanding work.

## Bring Into An OpenWrt Build Tree
1. Copy `openwrt/package/ee-wifi-autologin` into the OpenWrt build system, e.g. `feed/packages/net/` or `package/utils/`.
2. Run `./scripts/feeds update -a && ./scripts/feeds install python3 python3-requests python3-certifi` if using feeds.
3. Select the package: `make menuconfig` ? Network ? `ee-wifi-autologin` (depends on the Python interpreter).
4. Build firmware or an `ipk`: `make package/ee-wifi-autologin/{clean,compile} V=sc`.

### Using OpenWrt SDK
```bash
# inside the OpenWrt SDK root
cp -r /path/to/EE\ WIFI/openwrt/package/ee-wifi-autologin package/
./scripts/feeds update -a
./scripts/feeds install python3 python3-requests python3-certifi
make defconfig
make package/ee-wifi-autologin/compile V=sc
```
The resulting `ipk` will be under `bin/packages/*/base/`.

## Deploy On Router / VM
1. `scp` the built `ee-wifi-autologin_*.ipk` to the router (or `opkg install http://...`).
2. Copy the config template: `cp /etc/ee-wifi-autologin.json.example /etc/ee-wifi-autologin.json`.
3. Edit `/etc/ee-wifi-autologin.json` with real credentials and portal details (store secrets in a separate file if possible).
4. Enable service: `service ee-wifi-autologin enable`.
5. Start service: `service ee-wifi-autologin start`.
6. Tail logs: `logread -f | grep ee-wifi-autologin`.

## BT Business B2C Flow
The Python agent now implements a `bt_b2c` login handler that reproduces the Azure AD B2C workflow used by `auth.bt.com`.

Config fields required by the handler:
- `login_type`: set to `bt_b2c`.
- `portal_url`: EE splash page (`https://ee-wifi.ee.co.uk/home`).
- `init_url`: start of the BT flow, e.g. `https://ee-wifi.ee.co.uk/safLogon?safTenantKey=BTB`.
- `username` / `password`: BT Business credentials (store via `secrets_file` or environment variables).
- Optional overrides: `b2c_tenant`, `b2c_policy`, `init_method`, `init_headers`, `init_payload`. Normally these are derived automatically from the redirect chain.

Runtime notes:
- The agent follows the redirect to the B2C authorize page, posts credentials to the `SelfAsserted` endpoint (using the captured `x-ms-cpim-csrf` cookie), then submits the hidden callback form to `https://ee-wifi.ee.co.uk/safCallback/...`.
- Any change in the portal flow (new hidden inputs, extra MFA steps) will require updating the handler.
- Sanitise captures (`openwrt/chormelog.md`) after extracting field names?remove real passwords before committing.

## Quick Manual Test Inside OpenWrt
```bash
python3 /usr/share/ee-wifi-autologin/ee_wifi_autologin.py \
  --config /etc/ee-wifi-autologin.json \
  --once --verbose
```
Expect to see:
- Init request to `safLogon`.
- `SelfAsserted` POST returning `status: 200` and a redirect URL.
- Callback submission to `safCallback` followed by connectivity restoration.

## Next Steps
- Tune the `bt_b2c` handler once you verify the latest portal responses (extra tokens, MFA prompts, etc.).
- Move credentials into `/etc/ee-wifi-autologin.secrets.json` and reference via `secrets_file`.
- Add optional interface management (e.g. toggle `ifup wwan` before login attempts).
- Consider lightweight logging to `/var/log/ee-wifi-autologin.log` with rotation.
