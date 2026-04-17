#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

from urok_common import PROFILE_URL, WORKSPACE_ROOT, build_lightpanda_cookie_jar, login_session

LIGHTPANDA_BIN = WORKSPACE_ROOT / "tools" / "lightpanda" / "lightpanda"


def main() -> None:
    if not LIGHTPANDA_BIN.exists():
        raise RuntimeError(f"Lightpanda binary not found at {LIGHTPANDA_BIN}")

    session = login_session()
    with tempfile.TemporaryDirectory(prefix="urok-lightpanda-") as tmpdir:
        cookie_file = Path(tmpdir) / "cookies.json"
        build_lightpanda_cookie_jar(session, cookie_file)
        result = subprocess.run(
            [
                str(LIGHTPANDA_BIN),
                "fetch",
                "--cookie",
                str(cookie_file),
                "--dump",
                "markdown",
                "--wait-ms",
                "500",
                "--log-level",
                "error",
                PROFILE_URL,
            ],
            capture_output=True,
            text=True,
            check=True,
            timeout=120,
        )
    output = result.stdout
    markers = ["Личный кабинет", "Профиль пользователя", "alyonka.ivanova105@gmail.com"]
    missing = [marker for marker in markers if marker not in output]
    if missing:
        raise RuntimeError(f"Lightpanda output missing markers: {missing}")
    print(
        json.dumps(
            {
                "solution": "lightpanda",
                "url": PROFILE_URL,
                "bytes": len(output.encode("utf-8")),
                "markers": markers[:2],
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
