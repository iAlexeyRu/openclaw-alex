#!/usr/bin/env python3
from __future__ import annotations

import json

import requests

URL = "https://react-shopping-cart-67954.firebaseapp.com/"
MARKERS = [
    r"16 Product(s) found",
    "Cropped Stay Groovy off white",
    "Add to cart",
    "Free shipping",
]


def main() -> None:
    response = requests.get(URL, timeout=30)
    response.raise_for_status()
    html = response.text
    found = [marker for marker in MARKERS if marker in html]
    print(
        json.dumps(
            {
                "solution": "requests",
                "url": response.url,
                "status_code": response.status_code,
                "bytes": len(response.content),
                "markers_found": found,
                "markers_found_count": len(found),
                "markers_total": len(MARKERS),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
