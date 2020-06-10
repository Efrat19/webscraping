import logging
import os

from selenium import webdriver

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

executable_path_phantomjs = '/Users/idan.narotzki/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs'
executable_firefox = '/Users/idan.narotzki/Downloads/firefox'

url = 'https://www.misim.gov.il/svinfonadlan2010/InfoNadlanPerutWithMap.aspx?ProcessKey=3e778b47-d2ae-4546-a992-fa50cb00663b'

hebrew_city = 'חיפה'
driver = webdriver.Firefox()
driver.get(url)
