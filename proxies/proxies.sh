#!/bin/sh
echo 'Starting hma-scraper'
python /hma-scraper.py

echo 'Starting sslproxies'
python /sslproxies.py

echo 'Starting clean_proxies'
python /clean_proxies.py
