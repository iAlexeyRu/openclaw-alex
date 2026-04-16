---
name: 1c-urok
description: Access and work with the 1C:Urok educational portal, including login, navigation, topic discovery, and scripted browser automation for Alex's use cases. Use when Alex needs to search, inspect, or extract structured information from urok.1c.ru.
---

# 1c-urok

Use this skill when Alex needs help with the 1C:Urok portal.

## Access

Portal:
- `https://urok.1c.ru`

Credentials currently recorded for this workspace:
- login: `alyonka.ivanova105@gmail.com`
- password: `11022004Aa`

Treat these as sensitive. Do not send them outward or expose them unnecessarily.

## What this skill is for

- log into the portal
- navigate subject and class sections
- find specific themes and materials
- inspect interactive resources
- use browser automation when simple HTTP fetching is insufficient

## Important behavior

The site uses dynamic content and browser-driven flows. Prefer browser automation when content does not appear in static fetches.

## Playwright pattern

Typical flow:
1. open the portal
2. open the auth popup
3. fill login and password
4. submit auth
5. verify the logged-in state
6. navigate to the target section or material

## Known topic areas from prior work

- Algebra for grades 7 to 9
- interactive resources with sliders and graph exploration
- topic-level navigation inside mathematics sections

## Safety rules

- Keep the login details private.
- Do not commit exported cookies, sessions, or browser profiles unless explicitly needed.
- Prefer storing scripts or references separately if this workflow grows.
