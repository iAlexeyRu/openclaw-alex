#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from urok_common import WORKSPACE_ROOT

LIGHTPANDA_BIN = WORKSPACE_ROOT / "tools" / "lightpanda" / "lightpanda"


def extract_heading(markdown: str) -> str | None:
    lines = [line.strip() for line in markdown.splitlines() if line.strip()]
    for line in lines:
        if line.startswith("#"):
            return line.lstrip("#").strip()
    for line in lines:
        if line.startswith(("![", "[", "- ")):
            continue
        if len(line) < 10:
            continue
        return line[:200]
    for line in lines:
        return line[:200]
    return None


def run_fetch(url: str, wait_ms: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            str(LIGHTPANDA_BIN),
            "fetch",
            "--dump",
            "markdown",
            "--wait-ms",
            str(wait_ms),
            "--log-level",
            "error",
            url,
        ],
        capture_output=True,
        text=True,
        timeout=180,
        check=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--wait-ms", type=int, default=800)
    args = parser.parse_args()

    if not LIGHTPANDA_BIN.exists():
        raise RuntimeError(f"Lightpanda binary not found at {LIGHTPANDA_BIN}")

    used_wait_ms = args.wait_ms
    result = run_fetch(args.url, used_wait_ms)
    output = result.stdout
    if not output.strip():
        used_wait_ms = args.wait_ms + 400
        result = run_fetch(args.url, used_wait_ms)
        output = result.stdout

    print(
        json.dumps(
            {
                "solution": "lightpanda",
                "url": args.url,
                "bytes": len(output.encode("utf-8")),
                "heading": extract_heading(output),
                "stderr_bytes": len(result.stderr.encode("utf-8")),
                "used_wait_ms": used_wait_ms,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
