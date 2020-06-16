import pprint

from browsermobproxy import Server
from selenium import webdriver


class ProxyManager:
    __BMP = '/Users/idan.narotzki/Downloads/browsermob-proxy-2.1.4/bin/browsermob-proxy.bat'

    def __init__(self):
        self.__server = Server(ProxyManager.__BMP)  # ProxyManager.__BMP
        self.__client = None

    def start_server(self):
        self.__server.start()
        return self.__server

    def start_client(self):
        self.__client = self.__server.create_proxy(params={"trustAllServers": "true"})
        return self.__client

    @property
    def client(self):
        return self.__client

    @property
    def server(self):
        return self.__server


proxy = ProxyManager()
proxy.enableHarCaptureTypes(CaptureType.REQUEST_CONTENT, CaptureType.RESPONSE_CONTENT);
server = proxy.start_server()
client = proxy.start_client()

misim_url = 'https://www.misim.gov.il/svinfonadlan2010/startpageNadlanNewDesign.aspx?ProcessKey=3e778b47-d2ae-4546-a992-fa50cb00663b'
google_url = 'https://google.com'

client.new_har(misim_url)
print(client.proxy)

options = webdriver.FirefoxOptions()
options.add_argument("--proxy-server={}".format(client.proxy))
driver = webdriver.Firefox(firefox_options=options)
driver.get(misim_url)
# time.sleep(3)


pprint.pprint(client.har)
pprint.pprint(proxy.client)

server.stop()
