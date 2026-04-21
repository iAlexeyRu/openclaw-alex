---
name: vps-tw01
description: Operate and document Alex's VPS tw01, especially SSH access patterns, Docker workloads, deployment checks, logs, and service troubleshooting. Use when working on the VPS host, remote Docker services, deploy flows, or host-level diagnostics.
---

# vps-tw01

Use this skill for Alex's VPS named `tw01`.

## Keep secrets out of the skill

Do not store private keys, passwords, or tokens here. Use configured SSH access and local secret sources.

## What this skill is for

- inspect host health
- review Docker containers and images
- assist with deploy and restart workflows
- collect logs
- document the role of services on the VPS

## Preferred workflow

1. Confirm the target host really is `tw01`.
2. Start with read-only inspection unless an action is requested.
3. Check system health, uptime, disk, and container state.
4. For deploy work, identify compose path, runtime dependencies, and rollback path.
5. After changes, verify services are healthy.

## Command patterns

Examples only, adapt to the actual SSH alias or configured key:

```bash
ssh deploy@HOST "uname -a && uptime && df -h"
```

```bash
ssh deploy@HOST "docker ps -a && docker images"
```

```bash
ssh deploy@HOST "cd /path/to/app && docker compose up -d"
```

```bash
ssh deploy@HOST "docker logs CONTAINER --tail 100"
```

## Safety rules

- Do not assume deployment paths.
- Do not prune, rebuild, or restart broadly unless requested.
- Prefer targeted inspection before operational changes.
- Record stable host facts in references rather than hardcoding them in the skill body.
