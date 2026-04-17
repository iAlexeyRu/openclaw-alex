# URL benchmark set

Generated at: 2026-04-17T19:23:04Z
Runs per solution: 3
Lightpanda wait-ms: 800

| Site | requests mean, s | lightpanda mean, s | Faster | requests RSS, MB | lightpanda RSS, MB | requests status |
| --- | ---: | ---: | --- | ---: | ---: | ---: |
| meduza-io-feature-2026-04-17-iran-vremenno-otkryl-ormuzskiy-proliv-no-ssha-prodolzhayut-blokadu-k-chemu-eto-privedet | 0.591 | 1.125 | requests | 33.27 | 74.63 | 200 |
| github-com-openclaw-openclaw | 0.693 | 1.03 | requests | 33.57 | 89.19 | 200 |
| www-championat-com-football-article-6435656-rostov-sochi-0-1-obzor-matcha-25-go-tura-rpl-video-gola-zaika-statistika-tab | 0.184 | 1.181 | requests | 32.54 | 159.22 | 403 |
| store-steampowered-com-app-2427700-Backpack_Battles | 0.632 | 2.304 | requests | 32.93 | 104.95 | 200 |

## https://meduza.io/feature/2026/04/17/iran-vremenno-otkryl-ormuzskiy-proliv-no-ssha-prodolzhayut-blokadu-k-chemu-eto-privedet

- Faster: **requests**
- requests: 0.591s mean, 33.27 MB RSS mean, status 200, title: None
- lightpanda: 1.125s mean, 74.63 MB RSS mean, heading: Иран временно открыл Ормузский пролив, но США продолжают блокаду. К чему это приведет? Разбор «Медузы»

## https://github.com/openclaw/openclaw

- Faster: **requests**
- requests: 0.693s mean, 33.57 MB RSS mean, status 200, title: GitHub - openclaw/openclaw: Your own personal AI assistant. Any OS. Any Platform. The lobster way. 🦞 · GitHub
- lightpanda: 1.03s mean, 89.19 MB RSS mean, heading: Navigation Menu

## https://www.championat.com/football/article-6435656-rostov-sochi-0-1-obzor-matcha-25-go-tura-rpl-video-gola-zaika-statistika-tablica-17-aprelya-2026.html

- Faster: **requests**
- requests: 0.184s mean, 32.54 MB RSS mean, status 403, title: 403 Forbidden
- lightpanda: 1.181s mean, 159.22 MB RSS mean, heading: Для тех, кто любит спорт ](https://www.championat.com/page/app/)

## https://store.steampowered.com/app/2427700/Backpack_Battles/

- Faster: **requests**
- requests: 0.632s mean, 32.93 MB RSS mean, status 200, title: Backpack Battles on Steam
- lightpanda: 2.304s mean, 104.95 MB RSS mean, heading: Download Backpack Battles Demo

Notes:
- `requests` measures raw HTML fetch via Python requests.
- `lightpanda` measures rendered markdown via `lightpanda fetch --dump markdown`.
- CPU and RSS are approximate process-tree samples taken every 20 ms on this host.
- Cross-solution byte counts are not directly comparable because one side is HTML and the other is markdown output.