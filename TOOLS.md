# TOOLS.md - Local Notes

## Git

- Main repo: `git@github.com:iAlexeyRu/openclaw-alex.git`
- GitHub SSH key for this host: `~/.ssh/id_ed25519_openclaw_github`
- Public key comment: `alice@openclaw github access`
- Current public key path: `~/.ssh/id_ed25519_openclaw_github.pub`

## Messaging

- Primary communication channel for now: Telegram

## Notes

- This repository is intended to store the real ongoing workspace, not just bootstrap files.
- Commit useful workspace state when it helps continuity.
- Current rule for `.openclaw/`: keep `.openclaw/workspace-state.json`, avoid committing other runtime-only state unless we explicitly decide otherwise.
- Avoid committing secrets, tokens, caches, or runtime-only state.
