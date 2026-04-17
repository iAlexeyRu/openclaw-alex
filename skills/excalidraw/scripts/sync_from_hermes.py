#!/usr/bin/env python3
"""Sync the local Excalidraw skill from the Hermes upstream repo.

This keeps our vendored skill close to:
https://github.com/NousResearch/hermes-agent/tree/main/skills/creative/excalidraw

It applies a tiny local normalization for OpenClaw after download.

Usage:
    python3 skills/excalidraw/scripts/sync_from_hermes.py
    python3 skills/excalidraw/scripts/sync_from_hermes.py --check
"""

from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

RAW_BASE = "https://raw.githubusercontent.com/NousResearch/hermes-agent/main/skills/creative/excalidraw/"
FILES = [
    "SKILL.md",
    "references/colors.md",
    "references/dark-mode.md",
    "references/examples.md",
    "scripts/upload.py",
]
SKILL_ROOT = Path(__file__).resolve().parents[1]


def fetch_text(relative_path: str) -> str:
    with urllib.request.urlopen(RAW_BASE + relative_path, timeout=30) as response:
        return response.read().decode("utf-8")


def normalize(relative_path: str, content: str) -> str:
    if relative_path == "SKILL.md":
        content = content.replace(
            "3. **Save the file** using `write_file` to create a `.excalidraw` file\n"
            "4. **Optionally upload** for a shareable link using `scripts/upload.py` via `terminal`\n",
            "3. **Save the file** using `write` to create a `.excalidraw` file\n"
            "4. **Optionally upload** for a shareable link using `scripts/upload.py`\n",
        )
        content = content.replace(
            "Wrap your elements array in the standard `.excalidraw` envelope and save with `write_file`:\n",
            "Wrap your elements array in the standard `.excalidraw` envelope and save with `write`:\n",
        )
        content = content.replace(
            "```bash\npython skills/diagramming/excalidraw/scripts/upload.py ~/diagrams/my_diagram.excalidraw\n```\n",
            "```bash\npython3 skills/excalidraw/scripts/upload.py ~/diagrams/my_diagram.excalidraw\n```\n",
        )
    return content


def sync(check_only: bool = False) -> int:
    changed = []
    for relative_path in FILES:
        remote = normalize(relative_path, fetch_text(relative_path))
        local_path = SKILL_ROOT / relative_path
        local = local_path.read_text(encoding="utf-8") if local_path.exists() else None
        if local != remote:
            changed.append(relative_path)
            if not check_only:
                local_path.parent.mkdir(parents=True, exist_ok=True)
                local_path.write_text(remote, encoding="utf-8")

    if changed:
        verb = "would update" if check_only else "updated"
        for relative_path in changed:
            print(f"{verb}: {relative_path}")
        return 1 if check_only else 0

    print("Already up to date.")
    return 0


if __name__ == "__main__":
    raise SystemExit(sync(check_only="--check" in sys.argv[1:]))
