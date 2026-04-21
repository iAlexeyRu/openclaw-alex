---
name: proxmox-home
description: Work with Alex's home Proxmox environment, including host inventory, VM and LXC status checks, service mapping, and operational runbooks. Use when tasks involve the home lab, Proxmox resources, VM/LXC lifecycle, or documenting and troubleshooting the local infrastructure.
---

# proxmox-home

Use this skill for Alex's home Proxmox environment.

## Keep secrets out of the skill

Do not store API tokens, passwords, or private keys in this skill. Read them from the local environment, secret storage, or ask Alex when needed.

## What this skill is for

- map the home lab and its services
- inspect VM and LXC state
- document host roles and network layout
- suggest safe operational commands
- help troubleshoot reachability, service health, and routing problems

## Known home-lab shape

Current known structure:
- Proxmox node: `pve`
- router VM: OpenWrt
- Docker host LXC
- Ad-block/DNS LXC
- Amnezia/VPN LXC

Treat this as a starting point, not a guarantee. Re-check live state before making changes.

## Preferred workflow

1. Identify whether the task is read-only inspection or a state-changing action.
2. For inspection, gather current VM/LXC inventory and status first.
3. For actions, confirm the target node/VMID/container and expected impact.
4. Prefer the least risky action that answers the question.
5. After changes, verify status and summarize what changed.

## Suggested data to maintain in references

Store environment-specific facts in references files, for example:
- host inventory
- VMID to service mapping
- network layout
- known maintenance procedures

## Command patterns

Use local environment variables or secret storage for credentials. Example patterns only:

```bash
curl -s -k "https://${PROXMOX_HOST}:${PROXMOX_PORT}/api2/json/cluster/resources" \
  -H "Authorization: PVEAPIToken=${TOKEN_ID}=${TOKEN_SECRET}"
```

```bash
curl -s -k -X POST "https://${PROXMOX_HOST}:${PROXMOX_PORT}/api2/json/nodes/${PROXMOX_NODE}/lxc/${VMID}/status/reboot" \
  -H "Authorization: PVEAPIToken=${TOKEN_ID}=${TOKEN_SECRET}"
```

## Safety rules

- Do not invent VMIDs, hostnames, or credentials.
- Do not reboot or stop services unless the task actually calls for it.
- Warn before disruptive actions.
- Update references when the infrastructure map changes.
