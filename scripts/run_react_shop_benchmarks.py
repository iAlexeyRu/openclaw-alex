#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from run_1c_urok_benchmarks import run_once, summarize

ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = ROOT / "state" / "benchmarks"
REQUESTS_SCRIPT = ROOT / "scripts" / "react_shop_requests_check.py"
LIGHTPANDA_SCRIPT = ROOT / "scripts" / "react_shop_lightpanda_check.py"


def markdown_table(results: dict[str, Any]) -> str:
    lines = [
        "# React shopping cart render benchmark",
        "",
        f"Generated at: {results['generated_at']}",
        "",
        "| Solution | Runs ok | Mean elapsed, s | Mean CPU sec | Mean CPU % | Mean max RSS, MB | Markers found |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for name, data in results["solutions"].items():
        summary = data["summary"]
        elapsed = summary.get("elapsed_seconds", {}).get("mean", "-")
        cpu_seconds = summary.get("cpu_seconds", {}).get("mean", "-")
        cpu = summary.get("cpu_percent", {}).get("mean", "-")
        rss_kb = summary.get("max_rss_kb", {}).get("mean")
        rss_mb = round(rss_kb / 1024, 2) if rss_kb is not None else "-"
        first_payload = data["runs"][0].get("payload", {}) if data["runs"] else {}
        markers_found = f"{first_payload.get('markers_found_count', 0)}/{first_payload.get('markers_total', 0)}"
        lines.append(f"| {name} | {summary.get('ok_runs', 0)} | {elapsed} | {cpu_seconds} | {cpu} | {rss_mb} | {markers_found} |")
    lines.extend([
        "",
        "Notes:",
        "- Site: https://react-shopping-cart-67954.firebaseapp.com/",
        "- The selected markers live in the rendered product grid, not in the raw HTML shell.",
        "- `requests` measures raw HTML fetch only.",
        "- `lightpanda` measures rendered markdown after JavaScript execution.",
        "- CPU and RSS are approximate process-tree samples taken every 20 ms on this host.",
    ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=int, default=5)
    args = parser.parse_args()

    solutions = {
        "requests": REQUESTS_SCRIPT,
        "lightpanda": LIGHTPANDA_SCRIPT,
    }
    results: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "runs": args.runs,
        "solutions": {},
    }
    for name, script in solutions.items():
        runs = [run_once(script) for _ in range(args.runs)]
        results["solutions"][name] = {
            "runs": runs,
            "summary": summarize(runs),
        }

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    json_path = STATE_DIR / f"react-shop-benchmark-{stamp}.json"
    md_path = STATE_DIR / f"react-shop-benchmark-{stamp}.md"
    json_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(markdown_table(results), encoding="utf-8")

    print(json.dumps({"json": str(json_path), "markdown": str(md_path), "summary": results["solutions"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
