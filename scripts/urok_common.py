from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Tuple

import requests

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = WORKSPACE_ROOT / "skills" / "1c-urok" / "SKILL.md"
UROK_BASE = "https://urok.1c.ru"
LOGIN_URL = f"{UROK_BASE}/ajax/popupForm.php"
PROFILE_URL = f"{UROK_BASE}/personal/profile/"


def load_credentials() -> Tuple[str, str]:
    text = SKILL_PATH.read_text(encoding="utf-8")
    login_match = re.search(r"- login: `([^`]+)`", text)
    password_match = re.search(r"- password: `([^`]+)`", text)
    if not login_match or not password_match:
        raise RuntimeError("Could not load 1C:Urok credentials from skill file")
    return login_match.group(1), password_match.group(1)


def login_session() -> requests.Session:
    login, password = load_credentials()
    session = requests.Session()
    session.get(UROK_BASE, timeout=30)
    response = session.post(
        LOGIN_URL,
        headers={
            "X-Requested-With": "XMLHttpRequest",
            "Referer": f"{UROK_BASE}/",
        },
        data={
            "AUTH_FORM": "Y",
            "TYPE": "AUTH",
            "AJAX": "AUTH_FORM",
            "USER_LOGIN": login,
            "USER_PASSWORD": password,
            "USER_REMEMBER": "Y",
            "form_type": "auth",
        },
        timeout=30,
    )
    payload = response.json()
    if not payload.get("result"):
        raise RuntimeError(f"1C:Urok auth failed: {payload}")
    return session


def build_lightpanda_cookie_jar(session: requests.Session, cookie_path: Path) -> Path:
    cookies = []
    for cookie in session.cookies:
        if "urok.1c.ru" not in cookie.domain and not cookie.domain.endswith(".1c.ru"):
            continue
        cookies.append(
            {
                "name": cookie.name,
                "value": cookie.value,
                "domain": cookie.domain,
                "path": cookie.path,
                "expires": cookie.expires,
                "secure": cookie.secure,
                "httpOnly": False,
                "sameSite": "lax",
            }
        )
    cookie_path.write_text(json.dumps(cookies, ensure_ascii=False, indent=2), encoding="utf-8")
    return cookie_path
