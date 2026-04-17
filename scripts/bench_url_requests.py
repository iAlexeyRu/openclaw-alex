#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re

import requests


def extract_title(html: str) -> str | None:
    match = re.search(r"<title>(.*?)</title>", html, flags=re.I | re.S)
    if not match:
        return None
    return re.sub(r"\s+", " ", match.group(1)).strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    args = parser.parse_args()

    response = requests.get(args.url, timeout=45)
    print(
        json.dumps(
            {
                "solution": "requests",
                "url": args.url,
                "final_url": response.url,
                "status_code": response.status_code,
                "bytes": len(response.content),
                "title": extract_title(response.text),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
