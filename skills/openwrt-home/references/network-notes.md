# OpenWrt home notes

Safe, non-secret notes about Alex's home router.

## Current known patterns

- Router is a VM in the home lab
- LAN and WAN are separated
- VPN is used selectively for some traffic rather than always-on default routing
- Internal DNS forwarding may point to a local filtering resolver
- DPI-bypass tooling may affect latency for some services

## Troubleshooting hints

- If Telegram or similar apps feel slow, check policy routing and DPI-bypass behavior first.
- Verify whether DNS forwarding and firewall forwarding still match the intended topology.
