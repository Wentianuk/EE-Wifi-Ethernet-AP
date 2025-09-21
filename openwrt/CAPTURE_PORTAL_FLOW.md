# Capturing EE WiFi Captive Portal Flow

This guide walks through recording the real HTTP exchange during a successful EE WiFi / BT Business login so we can reproduce it from OpenWrt. Complete the capture on a laptop or VM that can already authenticate (e.g. the Windows environment that runs the original Selenium flow).

## 1. Prepare A Clean Session
- Forget/disable any saved EE WiFi credentials so the captive portal is triggered.
- Close all browser windows that might already be signed in.
- Optionally start a packet capture (`tcpdump`/`Wireshark`) on the interface to archive raw traffic when debugging.

## 2. Capture Via Browser DevTools (Recommended)
1. Connect to the EE WiFi hotspot.
2. Open Chrome (or Edge/Firefox) and go to any HTTP site (e.g. `http://neverssl.com`) to force the portal redirect.
3. Press `F12` to open Developer Tools ? **Network** tab.
4. Check **Preserve log** and **Disable cache** to keep all requests.
5. Complete the BT Business login as usual.
6. Identify the requests responsible for authentication:
   - Look for POST/GET requests to `ee-wifi.ee.co.uk`, `btopenzone.com`, or Microsoft OAuth endpoints.
   - Successful login usually returns HTTP 200/302 with tokens or redirect to `success` page.
7. Right-click the relevant request ? **Copy** ? `Copy as cURL` (bash). Paste it into a text file for later analysis.
8. Also copy response bodies/headers (right-click ? `Save all as HAR` for complete capture).

## 3. Analyse The Request
- Inspect the copied cURL command:
  - **URL**: this becomes `post_url` or `get_url`.
  - **Headers**: replicate mandatory ones (User-Agent, Referer, Content-Type, any authorization tokens).
  - **Form data**: note field names (`username`, `password`, hidden tokens like `PPFT`, `client_id`).
- If the flow uses Microsoft OAuth:
  - First request to the portal will redirect to `login.microsoftonline.com`.
  - You may need to reproduce the entire sequence (initial GET ? hidden form POST ? final POST). In that case consider switching to a scripted flow (e.g. `requests` with `session`) that mirrors each redirect.

## 4. Convert Into Config Entries
Update `/etc/ee-wifi-autologin.json` on OpenWrt (or the example template) with values from the capture:
```json
{
  "hotspots": [
    {
      "ssid": "EE WiFi",
      "login_type": "http_post",
      "portal_url": "https://ee-wifi.ee.co.uk/home",
      "post_url": "https://login.microsoftonline.com/common/oauth2/v2.0/token", 
      "headers": {
        "User-Agent": "Mozilla/5.0 ...",
        "Referer": "https://..."
      },
      "form_data": {
        "username": "lawrence@berriescoffee.co.uk",
        "password": "luqian66",
        "client_id": "<value from capture>",
        "scope": "<value>",
        "grant_type": "password",
        "tenant": "<value>",
        "PPFT": "{ppft_token}"
      },
      "success_status": [200, 302],
      "success_text": "You are connected"
    }
  ]
}
```
Adjust fields to match the actual capture. If dynamic tokens (e.g. `PPFT`, anti-CSRF) appear, capture how they are delivered (often via hidden inputs in a prior GET) and extend the Python agent to fetch them before posting.

## 5. Validate Manually
On a machine with Python installed (Windows or OpenWrt VM):
```bash
python3 ee_wifi_autologin.py --config ee-wifi-autologin.json --once --verbose
```
Watch the logs for the exact request/response codes. If the portal still redirects to login, compare headers/body with the captured browser request and adjust accordingly.

## 6. Advanced Capture Options
- **Mitmproxy**: run `mitmproxy --mode transparent` on a laptop and point the Windows VM through it; export the flow as Python code.
- **tcpdump/Wireshark**: filter on `host ee-wifi.ee.co.uk` to see raw HTTP; useful when HTTPS is terminated at the portal.
- **Selenium recording**: run the original Windows agent with debug logging or enable Chrome DevTools Protocol to export network HAR files automatically.

## 7. Keep Credentials Secure
- Never commit real usernames/passwords or HAR files with tokens into git.
- Strip access tokens or regenerate them before sharing.
- Use OpenWrt `secrets_file` or environment variables to store credentials outside the main config.

Once the capture reproduces successfully via `curl`/`requests`, paste the refined `headers` and `form_data` into the OpenWrt configuration and rebuild the package (or just update `/etc/ee-wifi-autologin.json` on the router).
