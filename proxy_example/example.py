import json
import os
import random
import time
from multiprocessing import Pool

from robobrowser import RoboBrowser
from robobrowser_wrapper import get_proxy_count, get_user_agent, open_url
from slack import slack_client

# using fake slack client that just prints to stdout
# provide SLACK_TOKEN and fake=False to use real slack integration
SLACK_ROOM = 'fake_slack'
sc = slack_client()


def parse_page(page):
    """
    Example parsing a page using random proxies/user_agents
    """
    time.sleep(random.uniform(0, .75))

    browser = RoboBrowser(
        history=False, parser='html5lib', user_agent=get_user_agent(),
        timeout=10
    )
    browser = open_url(browser, page)
    try:
        content = browser.find(id='mw-content-text')
        print(content.find('p').text)
    except:
        print("Error parsing {}".format(page))
        return page

    return None


def main():
    """
    Example main to template a worker pool
    Stores failed parses in a json file to go back a fix what failed
    Sends progess status to slack
    Replace pages and parse_page with your implementations
    """

    failed_pages = []
    failed_count = 0
    successful_count = 0

    pool = Pool(processes=int(get_proxy_count()/2))
    results = []
    failed_results = []
    pages = ["http://interstellarfilm.wikia.com/wiki/Ranger"]

    _ = [pool.apply_async(parse_page, (page,), callback=results.append, error_callback=failed_results.append) for page in pages]

    pool.close()
    progress = 0
    while len(results) + len(failed_results) < len(pages):
        if progress + 1000 <= len(results):
            progress = len(results)
            sc.api_call(
                "chat.postMessage",
                channel=SLACK_ROOM,
                text="Example: Finished {0} pages out of {1}".format(
                    len(results), len(pages)
                )
            )
        time.sleep(5)

    print("Uncaught exceptions: {}".format(failed_results))
    for response in results:
        if response is None:
            successful_count += 1
        else:
            failed_count += 1
            failed_pages.append(response)

    sc.api_call(
        "chat.postMessage",
        channel=SLACK_ROOM,
        text="Example pages scraped: {0}, failed {1}.".format(
            successful_count, failed_count
        )
    )

    failed_file = '/data/example/failed_pages.json'
    os.makedirs(os.path.dirname(failed_file), exist_ok=True)
    with open(failed_file, 'w') as output_file:
        json.dump(failed_pages, output_file)


if __name__ == '__main__':
    main()
