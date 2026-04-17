#!/usr/bin/env python3
from __future__ import annotations

import json
import re

from urok_common import PROFILE_URL, login_session


def extract_title(html: str) -> str | None:
    match = re.search(r"<title>(.*?)</title>", html, flags=re.I | re.S)
    if not match:
        return None
    return re.sub(r"\s+", " ", match.group(1)).strip()


def main() -> None:
    session = login_session()
    response = session.get(PROFILE_URL, timeout=30)
    response.raise_for_status()
    html = response.text
    markers = ["Личный кабинет", "Профиль пользователя"]
    missing = [marker for marker in markers if marker not in html]
    if missing:
        raise RuntimeError(f"Profile page missing markers: {missing}")
    print(
        json.dumps(
            {
                "solution": "requests",
                "url": response.url,
                "status_code": response.status_code,
                "title": extract_title(html),
                "bytes": len(response.content),
                "markers": markers,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
