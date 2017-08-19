## Scrape proxies
This docker container uses hma-scraper.py and sslproxies.py to scrape hidemyass.com and sslproxies.org to find free proxies. It combines both sites proxies and tests them against api.ipify.org using clean_proxies.py. It retries each proxy a maximum number of times to allow some failed requests while still making sure they are operational.

### Commands
`docker build -t proxy_scrape .`

`docker run -v $(pwd)/data:/data proxy_scrape`

### Output
Outputs in ['host:port', ...] to `./data/proxies.json`
