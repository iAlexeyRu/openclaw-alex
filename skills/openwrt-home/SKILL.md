---
name: openwrt-home
description: Operate and document Alex's home OpenWrt router, including routing, DHCP, firewall, DNS forwarding, VPN-related behavior, and connectivity troubleshooting. Use when tasks involve the home router, policy routing, VPN path selection, DNS behavior, or network debugging.
---

# openwrt-home

Use this skill for Alex's home OpenWrt router.

## Keep secrets out of the skill

Do not store router passwords, private keys, VPN private keys, or raw credentials in this skill. Read them from secure local sources when needed.

## What this skill is for

- inspect OpenWrt network state
- reason about LAN/WAN/VPN routing
- inspect DNS and DHCP behavior
- help troubleshoot firewall or policy-routing issues
- document stable network topology and known gotchas

## Known topology shape

Current known shape:
- OpenWrt runs as a home router VM
- LAN side serves Alex's local devices and service hosts
- there is a VPN path used for selected traffic rather than always as the default route
- DNS may be forwarded to an internal filtering resolver such as AdGuard

Treat these as working assumptions and verify live state before acting.

## Preferred workflow

1. Determine whether the task is inspection, troubleshooting, or a requested change.
2. For troubleshooting, check interface state, routes, firewall rules, and DNS behavior in that order.
3. For VPN issues, confirm whether policy-based routing or selective bypass is involved.
4. For performance complaints, consider whether DPI-bypass tooling, routing policy, or DNS latency is involved.
5. After changes, verify connectivity from the relevant path.

## Command patterns

```bash
ip addr && ip route
```

```bash
cat /etc/config/network
cat /etc/config/firewall
cat /etc/config/dhcp
```

```bash
logread | grep -E 'vpn|fw|dhcp|dns'
```

```bash
/etc/init.d/network reload
/etc/init.d/firewall reload
```

## Safety rules

- Do not store or echo private keys in notes.
- Do not change default routes casually.
- Warn before restarting networking on a live router.
- Record stable topology in references, not in ad hoc messages.
