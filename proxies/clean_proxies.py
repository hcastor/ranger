# Date created 2/27/16
import json
import os
import random
import time
from multiprocessing import Pool

from robobrowser import RoboBrowser


def testProxy(proxy):
    """
    Tests a proxy with api.ipify.org
    If the proxy fails, it retries 20 more times.
    This is because free proxies are unreliable at times.
    """
    tries = 0
    browser = RoboBrowser(history=False,  parser='html5lib', timeout=10)
    while(True):
        try:
            tries += 1
            browser.open("http://api.ipify.org", proxies={'http': proxy})
            if browser.find('body').text not in proxy:
                raise Exception('Failed')
            return proxy
        except:
            if tries > 20:
                return None
            time.sleep(random.uniform(.5, 2.5))


def get_proxy_list(path):
    proxies = []
    if os.path.isfile(path):
        with open(path, 'r') as old_proxies:
            proxies += json.load(old_proxies)
    return proxies


def main():
    """
    Used to get rid of any proxies that dont work anymore.
    Uses multiprocess to test 50 proxies at a time
    Overwrites ./data/proxies.json with only working proxies
    """
    pool = Pool(processes=50)

    results = []
    proxies = []
    # Combines sslproxies list and hma_proxies list into /run_data/proxies.json
    proxies += get_proxy_list('/run_data/hma_proxies.json')
    proxies += get_proxy_list('/run_data/ssl_proxies.json')
    proxies += get_proxy_list('/data/proxies.json')

    _ = [pool.apply_async(testProxy, (proxy,), callback=results.append) for proxy in proxies]

    pool.close()

    progress = 0
    while len(results) != len(proxies):
        if len(results) != progress:
            progress = len(results)
            print('Finished {} proxies out of {}'.format(len(results), len(proxies)))
        time.sleep(1)

    proxySet = set()
    duplicates = 0
    failed = 0
    success = 0
    with open('/data/proxies.json', 'w') as jsonFile:
        for proxy in results:
            if proxy:
                success += 1
                if proxy not in proxySet:
                    proxySet.add(proxy)
                else:
                    duplicates += 1
            else:
                failed += 1

        jsonFile.write(json.dumps(list(proxySet)))

    print('success:', success)
    print('failed:', failed)
    print('duplicates:', duplicates)
    print('total:', success - duplicates)


if __name__ == '__main__':
    main()
