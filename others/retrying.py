import time

from bs4 import BeautifulSoup as soup
from retry import retry

from proxy.random_proxy import Random_Proxy

start = time.time()

FIVE_MIN = 5 * 60
HOUR = 60 * 60


@retry(tries=-1, delay=10, max_delay=FIVE_MIN, backoff=2)
def foo(num):
    now = time.time()
    print("run foo with num={}".format(num))
    print("pass {} sec since start".format(now - start))
    if num == 0:
        print("g")
        num += 1
        time.sleep(1)
        assert num > 5


try:
    import requests
    from bs4 import BeautifulSoup
    import random

except:
    print(" Library Not Found !")

proxy = Random_Proxy()
url = 'https://www.yad2.co.il/realestate/forsale?city=4000&page=32'

# r = proxy.Proxy_Request(url=url, request_type="get")
# print(r)
# print(r.text)


# get the page soup

try:
    uClient = proxy.Proxy_Request(url=url, request_type='get')  # urlopen(url)
    page_html = uClient.text
    uClient.close()
except:
    raise
page_soup = soup(page_html, "html.parser")
print(page_soup.text)
