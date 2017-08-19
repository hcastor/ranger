import json
import os

from robobrowser import RoboBrowser


def main():
    browser = RoboBrowser(history=False,  parser='html5lib', timeout=10)

    browser.open("http://www.sslproxies.org/")

    # Finds the proxy table and zips the header with each row into a dict
    proxy_table = browser.find(id='proxylisttable')
    header = [each.text for each in proxy_table.find('thead').find_all('th')]
    rows = []
    for each in proxy_table.find('tbody').find_all('tr'):
        rows.append(dict(zip(header, [each.text for each in each.find_all('td')])))

    # Creates common http://ip:port format from hma-scrapper in proxies
    proxies = []
    for row in rows:
        proxy = 'http://{}:{}'.format(row['IP Address'], row['Port'])
        proxies.append(proxy)

    with open('/run_data/ssl_proxies.json', 'w') as proxies_file:
        json.dump(proxies, proxies_file)


if __name__ == '__main__':
    main()
