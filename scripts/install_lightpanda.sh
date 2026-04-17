#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INSTALL_DIR="$ROOT_DIR/tools/lightpanda"
BIN_PATH="$INSTALL_DIR/lightpanda"
VERSION_PATH="$INSTALL_DIR/VERSION"

mkdir -p "$INSTALL_DIR"

arch="$(uname -m)"
case "$arch" in
  x86_64|amd64)
    asset="lightpanda-x86_64-linux"
    ;;
  aarch64|arm64)
    asset="lightpanda-aarch64-linux"
    ;;
  *)
    echo "Unsupported architecture: $arch" >&2
    exit 1
    ;;
esac

url="https://github.com/lightpanda-io/browser/releases/download/nightly/${asset}"

echo "Installing Lightpanda from $url"
curl -fsSL "$url" -o "$BIN_PATH"
chmod +x "$BIN_PATH"
"$BIN_PATH" version | tee "$VERSION_PATH"
