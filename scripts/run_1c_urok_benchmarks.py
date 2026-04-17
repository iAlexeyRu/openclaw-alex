#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import statistics
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = ROOT / "state" / "benchmarks"
REQUESTS_SCRIPT = ROOT / "scripts" / "1c_urok_requests_check.py"
LIGHTPANDA_SCRIPT = ROOT / "scripts" / "1c_urok_lightpanda_check.py"
CLK_TCK = 100
PAGE_SIZE = 4096


def proc_children(pid: int) -> list[int]:
    path = Path(f"/proc/{pid}/task/{pid}/children")
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8").strip()
    return [int(item) for item in text.split() if item.strip()]


def proc_tree(root_pid: int) -> list[int]:
    seen: set[int] = set()
    stack = [root_pid]
    while stack:
        pid = stack.pop()
        if pid in seen:
            continue
        if not Path(f"/proc/{pid}").exists():
            continue
        seen.add(pid)
        stack.extend(proc_children(pid))
    return sorted(seen)


def proc_usage(pid: int) -> tuple[int, int]:
    stat_path = Path(f"/proc/{pid}/stat")
    if not stat_path.exists():
        return 0, 0
    text = stat_path.read_text(encoding="utf-8")
    rparen = text.rfind(")")
    rest = text[rparen + 2 :].split()
    utime = int(rest[11])
    stime = int(rest[12])
    rss_pages = int(rest[21])
    return utime + stime, rss_pages * PAGE_SIZE


def sample_tree(root_pid: int) -> tuple[float, int]:
    total_ticks = 0
    total_rss = 0
    for pid in proc_tree(root_pid):
        ticks, rss = proc_usage(pid)
        total_ticks += ticks
        total_rss += rss
    return total_ticks / CLK_TCK, total_rss


def measure_command(cmd: list[str]) -> tuple[subprocess.CompletedProcess[str], dict[str, Any]]:
    start = time.perf_counter()
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    peak_rss = 0
    cpu_samples: list[float] = []
    while proc.poll() is None:
        cpu_seconds, rss_bytes = sample_tree(proc.pid)
        cpu_samples.append(cpu_seconds)
        peak_rss = max(peak_rss, rss_bytes)
        time.sleep(0.02)
    stdout, stderr = proc.communicate(timeout=30)
    elapsed = time.perf_counter() - start
    final_cpu_seconds = cpu_samples[-1] if cpu_samples else 0.0
    cpu_percent = (final_cpu_seconds / elapsed * 100.0) if elapsed > 0 else 0.0
    completed = subprocess.CompletedProcess(cmd, proc.returncode, stdout, stderr)
    metrics = {
        "elapsed_seconds": round(elapsed, 3),
        "cpu_seconds": round(final_cpu_seconds, 3),
        "cpu_percent": round(cpu_percent, 3),
        "max_rss_kb": int(peak_rss / 1024),
    }
    return completed, metrics


def run_once(script_path: Path) -> dict[str, Any]:
    cmd = [sys.executable, str(script_path)]
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


def summarize(runs: list[dict[str, Any]]) -> dict[str, Any]:
    ok_runs = [run for run in runs if run["returncode"] == 0]
    if not ok_runs:
        return {"ok_runs": 0, "failed_runs": len(runs)}

    def values(key: str) -> list[float]:
        return [run["metrics"][key] for run in ok_runs if key in run["metrics"]]

    summary = {
        "ok_runs": len(ok_runs),
        "failed_runs": len(runs) - len(ok_runs),
    }
    for key in ["elapsed_seconds", "cpu_seconds", "cpu_percent", "max_rss_kb"]:
        nums = values(key)
        if nums:
            summary[key] = {
                "min": round(min(nums), 3),
                "max": round(max(nums), 3),
                "mean": round(statistics.mean(nums), 3),
                "median": round(statistics.median(nums), 3),
            }
    return summary


def markdown_table(results: dict[str, Any]) -> str:
    lines = [
        "# 1C:Urok benchmark",
        "",
        f"Generated at: {results['generated_at']}",
        "",
        "| Solution | Runs ok | Mean elapsed, s | Mean CPU sec | Mean CPU % | Mean max RSS, MB |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for name, data in results["solutions"].items():
        summary = data["summary"]
        elapsed = summary.get("elapsed_seconds", {}).get("mean", "-")
        cpu_seconds = summary.get("cpu_seconds", {}).get("mean", "-")
        cpu = summary.get("cpu_percent", {}).get("mean", "-")
        rss_kb = summary.get("max_rss_kb", {}).get("mean")
        rss_mb = round(rss_kb / 1024, 2) if rss_kb is not None else "-"
        lines.append(f"| {name} | {summary.get('ok_runs', 0)} | {elapsed} | {cpu_seconds} | {cpu} | {rss_mb} |")
    lines.extend([
        "",
        "Notes:",
        "- Scenario for both solutions: authenticate against 1C:Urok and open the protected profile page.",
        "- `requests` uses direct HTTP/AJAX auth plus a profile GET.",
        "- `lightpanda` uses the same auth step to mint cookies, then opens the same protected page through Lightpanda fetch.",
        "- CPU and RSS are approximate process-tree samples taken every 20 ms on this host.",
    ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=int, default=3)
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
    json_path = STATE_DIR / f"1c-urok-benchmark-{stamp}.json"
    md_path = STATE_DIR / f"1c-urok-benchmark-{stamp}.md"
    json_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(markdown_table(results), encoding="utf-8")

    print(json.dumps({"json": str(json_path), "markdown": str(md_path), "summary": results["solutions"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
