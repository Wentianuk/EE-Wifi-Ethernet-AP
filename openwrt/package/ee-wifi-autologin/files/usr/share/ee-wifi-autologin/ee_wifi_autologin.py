#!/usr/bin/env python3
"""Lightweight EE WiFi auto-login agent for OpenWrt."""

import argparse
import json
import logging
import os
import subprocess
import sys
import time
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, Iterable, Optional, Tuple
from urllib.parse import parse_qs, urljoin, urlparse

import requests

DEFAULT_CONFIG_PATH = "/etc/ee-wifi-autologin.json"
DEFAULT_CHECK_INTERVAL = 60
DEFAULT_CONNECTIVITY_URLS = [
    "https://connectivitycheck.gstatic.com/generate_204",
    "https://www.google.com/generate_204"
]
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


class HiddenFormParser(HTMLParser):
    """Parse the first HTML form and collect hidden inputs."""

    def __init__(self) -> None:
        super().__init__()
        self.in_form = False
        self.captured = False
        self.action: Optional[str] = None
        self.method: str = "GET"
        self.inputs: Dict[str, str] = {}

    def handle_starttag(self, tag: str, attrs):
        if self.captured:
            return
        attr_dict = dict(attrs)
        if tag.lower() == "form" and not self.in_form:
            self.in_form = True
            self.action = attr_dict.get("action")
            self.method = attr_dict.get("method", "POST").upper()
        elif tag.lower() == "input" and self.in_form:
            name = attr_dict.get("name")
            value = attr_dict.get("value", "")
            if name:
                self.inputs[name] = value

    def handle_endtag(self, tag: str):
        if tag.lower() == "form" and self.in_form:
            self.in_form = False
            self.captured = True


def setup_logging(verbose: bool = False) -> None:
    """Configure logging to stdout so procd can collect it."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def load_json(path: Path) -> Dict:
    """Load JSON configuration from disk."""
    if not path.exists():
        raise FileNotFoundError(f"Configuration file {path} not found")

    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


class AutoLoginAgent:
    """Main runner for connectivity checks and captive-portal login."""

    def __init__(self, config: Dict):
        self.config = config
        self.session = requests.Session()
        self.logger = logging.getLogger("AutoLoginAgent")
        timeouts = config.get("timeouts", {})
        self.http_timeout = timeouts.get("http", 8)
        self.login_timeout = timeouts.get("login", 30)
        self.check_interval = config.get("check_interval", DEFAULT_CHECK_INTERVAL)
        self.user_agent = config.get("user_agent", DEFAULT_USER_AGENT)

    # ------------------------------------------------------------------
    # Connectivity helpers
    # ------------------------------------------------------------------
    def connectivity_urls(self) -> Iterable[str]:
        urls = self.config.get("connectivity_urls")
        if urls:
            return urls
        return DEFAULT_CONNECTIVITY_URLS

    def check_connectivity(self) -> bool:
        """Return True when the internet appears reachable."""
        headers = {
            "User-Agent": self.user_agent,
            "Accept": "*/*",
        }
        for url in self.connectivity_urls():
            try:
                response = self.session.get(
                    url,
                    timeout=self.http_timeout,
                    allow_redirects=False,
                    headers=headers,
                )
                status = response.status_code
                location = response.headers.get("Location")
                self.logger.debug("Connectivity probe %s -> %s", url, status)
                if status in (200, 204) and not location:
                    return True
            except requests.RequestException as exc:
                self.logger.debug("Connectivity probe failed for %s: %s", url, exc)
        return False

    # ------------------------------------------------------------------
    # Command helpers
    # ------------------------------------------------------------------
    def run_commands(self, commands: Iterable[str], label: str) -> None:
        """Execute optional shell commands (best-effort)."""
        for command in commands:
            if not command:
                continue
            self.logger.info("Running %s command: %s", label, command)
            try:
                completed = subprocess.run(
                    command,
                    shell=True,
                    check=False,
                    capture_output=True,
                    text=True,
                )
                if completed.returncode != 0:
                    self.logger.warning(
                        "%s command failed (%s): %s",
                        label,
                        completed.returncode,
                        completed.stderr.strip(),
                    )
                elif completed.stdout:
                    self.logger.debug("%s output: %s", label, completed.stdout.strip())
            except Exception as exc:  # pragma: no cover - defensive
                self.logger.error("Error running %s command %s: %s", label, command, exc)

    # ------------------------------------------------------------------
    # Credential helpers
    # ------------------------------------------------------------------
    def resolve_credentials(self, hotspot: Dict) -> Dict[str, str]:
        """Merge credentials from hotspot config, secret file, and environment."""
        creds: Dict[str, str] = {}

        secret_file = hotspot.get("secrets_file")
        if secret_file and Path(secret_file).exists():
            try:
                with open(secret_file, "r", encoding="utf-8") as handle:
                    data = json.load(handle)
                if isinstance(data, dict):
                    creds.update({k: str(v) for k, v in data.items()})
            except Exception as exc:
                self.logger.warning("Failed to read secrets file %s: %s", secret_file, exc)

        for key in ("username", "password"):
            if key in hotspot:
                creds[key] = str(hotspot[key])
            env_key = hotspot.get(f"env_{key}")
            if env_key and env_key in os.environ:
                creds[key] = os.environ[env_key]

        return creds

    # ------------------------------------------------------------------
    # HTTP helpers
    # ------------------------------------------------------------------
    def build_headers(
        self,
        referer: Optional[str] = None,
        origin: Optional[str] = None,
        accept: Optional[str] = None,
        extra: Optional[Dict[str, str]] = None,
    ) -> Dict[str, str]:
        headers = {
            "User-Agent": self.user_agent,
            "Accept-Language": "en-GB,en;q=0.9",
        }
        headers["Accept"] = accept or "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        if referer:
            headers["Referer"] = referer
        if origin:
            headers["Origin"] = origin
        if extra:
            headers.update(extra)
        return headers

    # ------------------------------------------------------------------
    # Login helpers
    # ------------------------------------------------------------------
    def render_payload(self, template: Dict[str, str], creds: Dict[str, str]) -> Dict[str, str]:
        rendered: Dict[str, str] = {}
        for key, value in template.items():
            if isinstance(value, str):
                rendered[key] = value.format(**creds)
            else:
                rendered[key] = value
        return rendered

    def http_post_login(self, hotspot: Dict) -> bool:
        portal_url = hotspot.get("portal_url")
        post_url = hotspot.get("post_url", portal_url)
        if not post_url:
            self.logger.error("Hotspot %s missing post_url", hotspot.get("ssid", "<unknown>"))
            return False

        headers = hotspot.get("headers", {})
        creds = self.resolve_credentials(hotspot)
        payload_template = hotspot.get("form_data", {})
        payload = self.render_payload(payload_template, creds)

        if portal_url:
            try:
                self.logger.debug("Priming session with %s", portal_url)
                self.session.get(
                    portal_url,
                    timeout=self.login_timeout,
                    headers=headers,
                    allow_redirects=True,
                )
            except requests.RequestException as exc:
                self.logger.warning("Portal preflight failed: %s", exc)

        try:
            response = self.session.post(
                post_url,
                data=payload,
                timeout=self.login_timeout,
                headers=headers,
                allow_redirects=True,
            )
            self.logger.info(
                "POST to %s returned %s", post_url, response.status_code
            )
        except requests.RequestException as exc:
            self.logger.error("Login POST failed for %s: %s", post_url, exc)
            return False

        return self.evaluate_success(hotspot, response)

    def http_get_login(self, hotspot: Dict) -> bool:
        url = hotspot.get("get_url") or hotspot.get("portal_url")
        if not url:
            self.logger.error("Hotspot %s missing get_url", hotspot.get("ssid", "<unknown>"))
            return False

        try:
            response = self.session.get(
                url,
                timeout=self.login_timeout,
                headers=hotspot.get("headers", {}),
                allow_redirects=True,
            )
            self.logger.info("GET %s -> %s", url, response.status_code)
        except requests.RequestException as exc:
            self.logger.error("Login GET failed for %s: %s", url, exc)
            return False

        return self.evaluate_success(hotspot, response)

    def bt_b2c_login(self, hotspot: Dict) -> bool:
        """Handle Azure AD B2C sign-in used by BT Business/EE portal."""
        creds = self.resolve_credentials(hotspot)
        username = creds.get("username")
        password = creds.get("password")
        if not username or not password:
            self.logger.error("bt_b2c login requires username and password")
            return False

        init_url = hotspot.get("init_url") or hotspot.get("portal_url")
        if not init_url:
            self.logger.error("bt_b2c login missing init_url/portal_url")
            return False

        init_method = hotspot.get("init_method", "POST").upper()
        init_headers = hotspot.get("init_headers") or {}
        init_payload = hotspot.get("init_payload") or {}

        self.logger.debug("Starting BT B2C flow via %s", init_url)
        try:
            if init_method == "POST":
                response = self.session.post(
                    init_url,
                    data=init_payload,
                    timeout=self.login_timeout,
                    headers=self.build_headers(origin=urlparse(init_url).scheme + "://" + urlparse(init_url).netloc, extra=init_headers),
                    allow_redirects=True,
                )
            else:
                response = self.session.get(
                    init_url,
                    params=init_payload,
                    timeout=self.login_timeout,
                    headers=self.build_headers(extra=init_headers),
                    allow_redirects=True,
                )
        except requests.RequestException as exc:
            self.logger.error("bt_b2c init call failed: %s", exc)
            return False

        authorize_url = response.url
        parsed = urlparse(authorize_url)
        tenant = hotspot.get("b2c_tenant")
        policy = hotspot.get("b2c_policy")
        tx_value = hotspot.get("b2c_tx")

        path_parts = [part for part in parsed.path.split("/") if part]
        if not tenant and len(path_parts) >= 2:
            tenant = path_parts[0]
            policy = policy or path_parts[1]
        query = parse_qs(parsed.query)
        tx_value = tx_value or query.get("tx", [None])[0]
        policy = policy or query.get("p", [None])[0]

        if not tenant or not policy or not tx_value:
            self.logger.error(
                "Unable to derive B2C tenant/policy/tx from %s", authorize_url
            )
            return False

        authority = f"{parsed.scheme}://{parsed.netloc}"
        self.logger.debug(
            "Derived B2C context tenant=%s policy=%s tx=%s", tenant, policy, tx_value
        )

        # Preflight SelfAsserted endpoint to establish cookies (including x-ms-cpim-csrf)
        self_asserted_params = {"tx": tx_value, "p": policy}
        self_asserted_url = f"{authority}/{tenant}/{policy}/SelfAsserted"
        try:
            self.session.get(
                self_asserted_url,
                params=self_asserted_params,
                timeout=self.login_timeout,
                headers=self.build_headers(
                    referer=authorize_url,
                    accept="application/json, text/javascript, */*; q=0.01",
                    extra={"X-Requested-With": "XMLHttpRequest"},
                ),
                allow_redirects=True,
            )
        except requests.RequestException as exc:
            self.logger.warning("SelfAsserted preflight failed: %s", exc)

        csrf_token = self.session.cookies.get("x-ms-cpim-csrf")
        if not csrf_token:
            self.logger.error("Missing x-ms-cpim-csrf cookie; cannot continue")
            return False

        payload = {
            "request_type": "RESPONSE",
            "signInName": username,
            "password": password,
        }

        try:
            login_response = self.session.post(
                self_asserted_url,
                params=self_asserted_params,
                data=payload,
                timeout=self.login_timeout,
                headers=self.build_headers(
                    referer=authorize_url,
                    origin=authority,
                    accept="application/json, text/javascript, */*; q=0.01",
                    extra={
                        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                        "X-Requested-With": "XMLHttpRequest",
                        "x-csrf-token": csrf_token,
                    },
                ),
                allow_redirects=True,
            )
        except requests.RequestException as exc:
            self.logger.error("SelfAsserted login failed: %s", exc)
            return False

        try:
            result_json = login_response.json()
        except ValueError:
            self.logger.error("Unexpected Non-JSON response from SelfAsserted endpoint")
            return False

        if result_json.get("status") not in (200, "200", "success"):
            self.logger.error("B2C login rejected: %s", result_json)
            return False

        redirect_url = result_json.get("redirectUrl") or result_json.get("url")
        if not redirect_url:
            self.logger.error("SelfAsserted response missing redirectUrl: %s", result_json)
            return False

        redirect_url = urljoin(authority, redirect_url)
        self.logger.debug("Following redirect %s", redirect_url)
        try:
            confirm_response = self.session.get(
                redirect_url,
                timeout=self.login_timeout,
                headers=self.build_headers(referer=authorize_url),
                allow_redirects=True,
            )
        except requests.RequestException as exc:
            self.logger.error("Failed to load redirectUrl %s: %s", redirect_url, exc)
            return False

        form_details = self.extract_form(confirm_response.text)
        if not form_details:
            self.logger.error("Unable to locate callback form in B2C response")
            return False

        form_action, form_method, form_inputs = form_details
        callback_url = urljoin(redirect_url, form_action)
        self.logger.debug(
            "Submitting callback form to %s with fields %s",
            callback_url,
            list(form_inputs.keys()),
        )

        try:
            if form_method == "POST":
                final_response = self.session.post(
                    callback_url,
                    data=form_inputs,
                    timeout=self.login_timeout,
                    headers=self.build_headers(
                        referer=redirect_url,
                        origin=urlparse(callback_url).scheme + "://" + urlparse(callback_url).netloc,
                        extra={"Content-Type": "application/x-www-form-urlencoded"},
                    ),
                    allow_redirects=True,
                )
            else:
                final_response = self.session.get(
                    callback_url,
                    params=form_inputs,
                    timeout=self.login_timeout,
                    headers=self.build_headers(referer=redirect_url),
                    allow_redirects=True,
                )
        except requests.RequestException as exc:
            self.logger.error("Callback submission failed: %s", exc)
            return False

        self.logger.info(
            "Callback to %s completed with status %s",
            callback_url,
            final_response.status_code,
        )
        return final_response.status_code in (200, 204, 302)

    def extract_form(self, html: str) -> Optional[Tuple[str, str, Dict[str, str]]]:
        parser = HiddenFormParser()
        parser.feed(html)
        if parser.action:
            return parser.action, parser.method, parser.inputs
        return None

    def evaluate_success(self, hotspot: Dict, response: requests.Response) -> bool:
        """Determine if login likely succeeded based on config hints."""
        success_codes = hotspot.get("success_status", [200, 204, 302])
        if isinstance(success_codes, int):
            success_codes = [success_codes]

        if response.status_code in success_codes:
            text_snippet = hotspot.get("success_text")
            if text_snippet:
                if text_snippet.lower() in response.text.lower():
                    return True
                self.logger.debug("Success text '%s' not found", text_snippet)
                return False
            return True

        self.logger.debug(
            "Response code %s not in expected %s", response.status_code, success_codes
        )
        return False

    def perform_login(self, hotspot: Dict) -> bool:
        login_type = hotspot.get("login_type", "http_post")

        pre_cmds = hotspot.get("pre_login_commands", [])
        if pre_cmds:
            self.run_commands(pre_cmds, "pre-login")

        success = False
        if login_type == "http_post":
            success = self.http_post_login(hotspot)
        elif login_type == "http_get":
            success = self.http_get_login(hotspot)
        elif login_type == "bt_b2c":
            success = self.bt_b2c_login(hotspot)
        else:
            self.logger.error("Unsupported login_type %s", login_type)

        post_cmds = hotspot.get("post_login_commands", [])
        if post_cmds:
            self.run_commands(post_cmds, "post-login")

        return success

    # ------------------------------------------------------------------
    # Main loops
    # ------------------------------------------------------------------
    def run_once(self) -> bool:
        if self.check_connectivity():
            self.logger.info("Connectivity OK; nothing to do")
            return True

        hotspots = self.config.get("hotspots", [])
        if not hotspots:
            self.logger.error("No hotspots configured")
            return False

        for hotspot in hotspots:
            ssid = hotspot.get("ssid", "<unknown>")
            self.logger.info("Attempting login for hotspot %s", ssid)
            try:
                if self.perform_login(hotspot):
                    self.logger.info("Login flow for %s completed; re-checking connectivity", ssid)
                    time.sleep(3)
                    if self.check_connectivity():
                        self.logger.info("Connectivity restored after %s login", ssid)
                        return True
                    self.logger.warning("Connectivity still down after %s login", ssid)
            except Exception as exc:  # pragma: no cover - defensive
                self.logger.error("Error handling hotspot %s: %s", ssid, exc)

        return False

    def run_forever(self) -> None:
        interval = max(5, int(self.check_interval))
        self.logger.info("Starting monitor loop (interval %ss)", interval)
        while True:
            self.run_once()
            time.sleep(interval)


def parse_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="EE WiFi auto-login agent for OpenWrt")
    parser.add_argument("--config", default=DEFAULT_CONFIG_PATH, help="Path to JSON configuration")
    parser.add_argument("--once", action="store_true", help="Run a single connectivity check and exit")
    parser.add_argument("--loop", action="store_true", help="Run continuously until interrupted")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")
    return parser.parse_args(argv)


def main(argv: Optional[Iterable[str]] = None) -> int:
    args = parse_args(argv)
    setup_logging(args.verbose)

    try:
        config = load_json(Path(args.config))
    except Exception as exc:
        logging.error("Failed to load configuration: %s", exc)
        return 1

    agent = AutoLoginAgent(config)

    if args.once and not args.loop:
        return 0 if agent.run_once() else 1

    try:
        agent.run_forever()
    except KeyboardInterrupt:
        logging.info("Interrupted; exiting")
    return 0


if __name__ == "__main__":
    sys.exit(main())
