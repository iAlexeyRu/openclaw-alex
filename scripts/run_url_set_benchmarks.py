#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from run_1c_urok_benchmarks import measure_command, summarize

ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = ROOT / "state" / "benchmarks"
REQUESTS_SCRIPT = ROOT / "scripts" / "bench_url_requests.py"
LIGHTPANDA_SCRIPT = ROOT / "scripts" / "bench_url_lightpanda.py"


def slugify_url(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path.strip("/").replace("/", "-")
    if not path:
        path = "root"
    return f"{parsed.netloc.replace('.', '-')}-{path}"[:120]


def run_cmd(cmd: list[str]) -> dict[str, Any]:
    proc, metrics = measure_command(cmd)
    stdout = proc.stdout.strip()
    payload = json.loads(stdout) if stdout else {}
    return {
        "command": cmd,
        "returncode": proc.returncode,
        "payload": payload,
        "metrics": metrics,
        "stderr_tail": "\n".join(proc.stderr.strip().splitlines()[-10:]),
    }


def mean_metric(runs: list[dict[str, Any]], key: str) -> float | None:
    nums = [run["metrics"][key] for run in runs if run.get("returncode") == 0 and key in run.get("metrics", {})]
    if not nums:
        return None
    return round(statistics.mean(nums), 3)


def site_summary_block(url: str, site_data: dict[str, Any]) -> list[str]:
    requests_summary = site_data["requests"]["summary"]
    lightpanda_summary = site_data["lightpanda"]["summary"]
    req_elapsed = requests_summary.get("elapsed_seconds", {}).get("mean")
    lp_elapsed = lightpanda_summary.get("elapsed_seconds", {}).get("mean")
    if req_elapsed is not None and lp_elapsed is not None:
        faster = "requests" if req_elapsed < lp_elapsed else "lightpanda"
    else:
        faster = "n/a"

    req_payload = site_data["requests"]["runs"][0].get("payload", {}) if site_data["requests"]["runs"] else {}
    lp_payload = site_data["lightpanda"]["runs"][0].get("payload", {}) if site_data["lightpanda"]["runs"] else {}

    lines = [
        f"## {url}",
        "",
        f"- Faster: **{faster}**",
        f"- requests: {req_elapsed}s mean, {round(requests_summary.get('max_rss_kb', {}).get('mean', 0) / 1024, 2)} MB RSS mean, status {req_payload.get('status_code')}, title: {req_payload.get('title')}",
        f"- lightpanda: {lp_elapsed}s mean, {round(lightpanda_summary.get('max_rss_kb', {}).get('mean', 0) / 1024, 2)} MB RSS mean, heading: {lp_payload.get('heading')}",
        "",
    ]
    return lines


def markdown_report(results: dict[str, Any]) -> str:
    lines = [
        "# URL benchmark set",
        "",
        f"Generated at: {results['generated_at']}",
        f"Runs per solution: {results['runs']}",
        f"Lightpanda wait-ms: {results['wait_ms']}",
        "",
        "| Site | requests mean, s | lightpanda mean, s | Faster | requests RSS, MB | lightpanda RSS, MB | requests status |",
        "| --- | ---: | ---: | --- | ---: | ---: | ---: |",
    ]
    for url, site_data in results["sites"].items():
        req = site_data["requests"]["summary"]
        lp = site_data["lightpanda"]["summary"]
        req_elapsed = req.get("elapsed_seconds", {}).get("mean", "-")
        lp_elapsed = lp.get("elapsed_seconds", {}).get("mean", "-")
        faster = "requests" if isinstance(req_elapsed, (int, float)) and isinstance(lp_elapsed, (int, float)) and req_elapsed < lp_elapsed else "lightpanda"
        req_rss = round(req.get("max_rss_kb", {}).get("mean", 0) / 1024, 2) if req.get("max_rss_kb") else "-"
        lp_rss = round(lp.get("max_rss_kb", {}).get("mean", 0) / 1024, 2) if lp.get("max_rss_kb") else "-"
        req_status = site_data["requests"]["runs"][0].get("payload", {}).get("status_code", "-")
        label = slugify_url(url)
        lines.append(f"| {label} | {req_elapsed} | {lp_elapsed} | {faster} | {req_rss} | {lp_rss} | {req_status} |")
    lines.append("")
    for url, site_data in results["sites"].items():
        lines.extend(site_summary_block(url, site_data))
    lines.extend([
        "Notes:",
        "- `requests` measures raw HTML fetch via Python requests.",
        "- `lightpanda` measures rendered markdown via `lightpanda fetch --dump markdown`.",
        "- CPU and RSS are approximate process-tree samples taken every 20 ms on this host.",
        "- Cross-solution byte counts are not directly comparable because one side is HTML and the other is markdown output.",
    ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("urls", nargs="+")
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--wait-ms", type=int, default=800)
    args = parser.parse_args()

    results: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "runs": args.runs,
        "wait_ms": args.wait_ms,
        "sites": {},
    }
    for url in args.urls:
        req_runs = [run_cmd([sys.executable, str(REQUESTS_SCRIPT), url]) for _ in range(args.runs)]
        lp_runs = [run_cmd([sys.executable, str(LIGHTPANDA_SCRIPT), "--wait-ms", str(args.wait_ms), url]) for _ in range(args.runs)]
        results["sites"][url] = {
            "requests": {"runs": req_runs, "summary": summarize(req_runs)},
            "lightpanda": {"runs": lp_runs, "summary": summarize(lp_runs)},
        }

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    json_path = STATE_DIR / f"url-benchmark-set-{stamp}.json"
    md_path = STATE_DIR / f"url-benchmark-set-{stamp}.md"
    json_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(markdown_report(results), encoding="utf-8")
    print(json.dumps({"json": str(json_path), "markdown": str(md_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
