# Lightpanda local tool

- Installer: `scripts/install_lightpanda.sh`
- Benchmark wrapper: `scripts/benchmark_1c_urok.sh`
- Binary path after install: `tools/lightpanda/lightpanda`
- Pinned version marker: `tools/lightpanda/VERSION`

Notes:
- The downloaded `lightpanda` binary is kept locally in the workspace.
- The binary itself is ignored in git to avoid bloating the repository with a 100MB+ vendor artifact.
- Re-run the installer any time you want to refresh the local binary.
