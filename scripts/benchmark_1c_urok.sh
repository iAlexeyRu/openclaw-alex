#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

"$ROOT_DIR/scripts/install_lightpanda.sh"
python3 "$ROOT_DIR/scripts/run_1c_urok_benchmarks.py" "$@"
