# Date created 2/16/16
import json
import random
import time


def open_url(browser, url):
    """
    Wraps browser.open
    Uses a random proxy per request
    tries 20 times to succeed, else waits 5 minutes then tries twice more.
    returns browser
    should abstract out 20 and 300
    """
    tries = 0
    while True:
        try:
            tries += 1

            browser.open(url, proxies={'http': get_proxy()})

            if browser.response.status_code != 200:
                raise Exception('Response Code: ' + str(browser.response.status_code))
        except:
            if tries == 2.1:
                return browser
            if tries > 20:
                tries = 0.1
                time.sleep(300)
            else:
                time.sleep(random.uniform(.5, 2.5))
            continue
        return browser


def get_proxy():
    """
    Reads /proxies.json and returns a random proxy ip:port.
    """
    proxies = []
    with open('/proxies.json', 'r') as jsonfile:
        proxies = json.load(jsonfile)

    return proxies[random.randint(0, len(proxies)-1)]


def get_proxy_count():
    """
    Reads /proxies.json and returns the total number of proxies.
    """

    with open('/proxies.json', 'r') as jsonfile:
        proxies = json.load(jsonfile)

        return len(proxies)


def get_user_agent():
    """
    Returns a random user_agent
    """
    user_agents = ["Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"]

    user_agent = user_agents[random.randint(0, len(user_agents)-1)]

    return user_agent
