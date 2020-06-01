import logging
import os

from selenium import webdriver
from selenium.webdriver.common.by import By

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

misim_url = 'https://www.misim.gov.il/svinfonadlan2010/startpageNadlanNewDesign.aspx?ProcessKey=3e778b47-d2ae-4546-a992-fa50cb00663b'
executable_path_phantomjs = '/Users/idan.narotzki/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs'
executable_firefox = '/Users/idan.narotzki/Downloads/firefox'

from bs4 import BeautifulSoup
from urllib.request import urlopen, urlretrieve
from urllib.parse import urljoin

misim_url = 'https://www.misim.gov.il/svinfonadlan2010/startpageNadlanNewDesign.aspx?ProcessKey=3e778b47-d2ae-4546-a992-fa50cb00663b'
soup = BeautifulSoup(urlopen(misim_url))
all_imgs = soup.find_all('img')
captcha_img = all_imgs[7]

img_url = urljoin(misim_url, captcha_img['src'])
file_name = captcha_img['src'].split('/')[-1]
r = urlretrieve(img_url, file_name)

# 3


driver = webdriver.Firefox()

driver.get(misim_url)

c = driver.find_element(By.ID, 'ContentUsersPage_RadCaptcha1_CaptchaImageUP')
imageHeight = c.size['height']
imageWidth = c.size['width']
image_string_bytes = c.screenshot_as_png

# im = Image.frombytes("RGB", (imageWidth, imageHeight), image_string_bytes)

# https://stackoverflow.com/questions/2323128/convert-string-in-base64-to-image-and-save-on-filesystem-in-python


options = webdriver.FirefoxOptions
