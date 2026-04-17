#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess

from urok_common import WORKSPACE_ROOT

URL = "https://react-shopping-cart-67954.firebaseapp.com/"
MARKERS = [
    r"16 Product\(s\) found",
    "Cropped Stay Groovy off white",
    "Add to cart",
    "Free shipping",
]
LIGHTPANDA_BIN = WORKSPACE_ROOT / "tools" / "lightpanda" / "lightpanda"


def main() -> None:
    result = subprocess.run(
        [
            str(LIGHTPANDA_BIN),
            "fetch",
            "--dump",
            "markdown",
            "--wait-ms",
            "1500",
            "--log-level",
            "error",
            URL,
        ],
        capture_output=True,
        text=True,
        check=True,
        timeout=180,
    )
    output = result.stdout
    found = [marker for marker in MARKERS if marker in output]
    print(
        json.dumps(
            {
                "solution": "lightpanda",
                "url": URL,
                "bytes": len(output.encode("utf-8")),
                "markers_found": found,
                "markers_found_count": len(found),
                "markers_total": len(MARKERS),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
