---
name: amnezia-install
description: Install and operate AmneziaWG on a VPS using Docker or Compose, including prerequisite checks, TUN validation, data-path setup, container launch, and post-install verification. Use when Alex wants to deploy or troubleshoot an AmneziaWG server on a VPS.
---

# amnezia-install

Use this skill to deploy or troubleshoot AmneziaWG on a VPS.

## Keep secrets out of the skill

Do not store private keys, SSH credentials, admin passwords, or issued VPN client configs in this skill.

## Inputs to gather

- target host or IP
- SSH port and user
- SSH auth method
- container name
- web UI port
- VPN UDP port
- subnet
- MTU
- data path on the host

## Preferred workflow

1. Confirm Docker is available on the target VPS.
2. Confirm `/dev/net/tun` exists and is usable.
3. Create or verify the data path.
4. Choose Compose or one-shot `docker run` deployment.
5. Start the service.
6. Verify container health and local HTTP status.
7. Remind Alex to rotate defaults and store resulting credentials safely.

## Command patterns

```bash
ssh -p PORT USER@HOST "uname -a && docker --version"
```

```bash
ssh -p PORT USER@HOST "[ -c /dev/net/tun ] && echo tun:ok || echo tun:miss"
```

```bash
ssh -p PORT USER@HOST "mkdir -p DATA_PATH"
```

## Compose shape

Use a container with:
- NET_ADMIN and SYS_MODULE capabilities
- `/dev/net/tun`
- IP forwarding sysctls
- persistent volume for Amnezia data
- mapped TCP web port and UDP VPN port

## Verification

```bash
ssh -p PORT USER@HOST "docker ps"
```

```bash
ssh -p PORT USER@HOST "curl -s http://localhost:WEB_PORT/api/system/status"
```

## Safety rules

- Do not leave default passwords unchanged after install.
- Do not assume TUN exists on every VPS.
- Do not overwrite an existing deployment without checking for existing state.
- Keep generated configs and credentials outside the repo unless explicitly sanitized.
