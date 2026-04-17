# React shopping cart render benchmark

Generated at: 2026-04-17T19:13:35Z

| Solution | Runs ok | Mean elapsed, s | Mean CPU sec | Mean CPU % | Mean max RSS, MB | Markers found |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| requests | 5 | 0.294 | 0.13 | 44.224 | 32.28 | 0/4 |
| lightpanda | 5 | 1.691 | 0.132 | 7.8 | 93.29 | 4/4 |

Notes:
- Site: https://react-shopping-cart-67954.firebaseapp.com/
- The selected markers live in the rendered product grid, not in the raw HTML shell.
- `requests` measures raw HTML fetch only.
- `lightpanda` measures rendered markdown after JavaScript execution.
- CPU and RSS are approximate process-tree samples taken every 20 ms on this host.