# AmneziaWG deploy notes

Safe deployment notes for AmneziaWG on a VPS.

## Checklist

- Docker installed
- `/dev/net/tun` available
- chosen web port open if external UI is intended
- chosen VPN UDP port open in host firewall/provider firewall
- persistent data path prepared
- admin password rotated after first login

## Reminder

Never commit generated VPN configs, admin credentials, or private keys.
