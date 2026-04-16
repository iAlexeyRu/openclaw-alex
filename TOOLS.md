# TOOLS.md - Local Notes

## Git

- Main repo: `git@github.com:iAlexeyRu/openclaw-alex.git`
- SSH key label/comment: `vi@openclaw.local`
- SSH private key path on this host: `/home/debian/.ssh/openclaw_vi_ed25519`

## Messaging

- Primary communication channel for now: Telegram

## Notes

- This repository is intended to store the real ongoing workspace, not just bootstrap files.
- Commit useful workspace state when it helps continuity.
- Current rule for `.openclaw/`: keep `.openclaw/workspace-state.json`, avoid committing other runtime-only state unless we explicitly decide otherwise.
- Avoid committing secrets, tokens, caches, or runtime-only state.
