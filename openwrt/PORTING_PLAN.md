# OpenWrt Porting Plan

## Current State
- Core automation depends on Windows-only tooling: 
etsh for WLAN control, PowerShell launchers, and Chrome/Selenium for captive-portal flows.
- Logging layer expects desktop resources (SQLite, large log files) and Windows file paths.
- Auto-start and monitoring scripts target the Windows task scheduler / startup folders.

## Constraints On OpenWrt
- BusyBox environment, limited storage/RAM, no native Chrome/Chromedriver.
- Wi-Fi interfaces managed through 
etifd/uci; captive portals must be handled via HTTP requests or CLI tools.
- Prefer lightweight dependencies already packaged for OpenWrt (Python 3, python3-requests, curl, iwinfo).

## Proposed Direction
1. **Split the project** into a platform-agnostic core and platform-specific adapters.
2. **Reimplement the captive-portal workflow** using direct HTTP requests (no Selenium). Capture the portal traffic on Windows first to replicate the sequence with equests.
3. **Replace 
etsh usage** with calls to ubus, uci, or iwinfo for interface status / reconnect logic.
4. **Trim logging** to a simple JSON/text log (SQLite is optional and heavy for routers).
5. **Introduce OpenWrt configuration** via /etc/ee-wifi-autologin.json plus an /etc/init.d service script.
6. **Package layout**: package/ee-wifi-autologin/Makefile + iles/usr/share/ee-wifi-autologin/ for Python, iles/etc/init.d/ for service, iles/etc/ee-wifi-autologin.json.example template.
7. **Runtime service**: loop script that checks connectivity (equests to known URLs), triggers login when offline, and sleeps between checks. Start via procd init script.

## Outstanding Research
- Exact HTTP flow for BT Business captive portal on EE WiFi (OAuth vs classic form).
- Whether credentials can be posted directly without Javascript or MSAL.
- Minimum packages needed on OpenWrt image (python3, python3-requests, maybe ca-bundle).

## Next Implementation Steps
1. Build a lightweight Python agent (ee_wifi_autologin.py) that implements connectivity checks and pluggable login handlers.
2. Add OpenWrt package skeleton with Makefile/install targets.
3. Provide init script + config template.
4. Validate inside the OpenWrt VM (install dependencies, run python3 /usr/share/... --once).

