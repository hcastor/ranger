FROM python:alpine

RUN mkdir -p /run_data

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY hma-scraper.py /
COPY sslproxies.py /
COPY clean_proxies.py /
COPY proxies.sh /
RUN chmod +x /proxies.sh
CMD ["/proxies.sh"]
