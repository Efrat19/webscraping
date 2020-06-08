import logging
import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

executable_path_phantomjs = '/Users/idan.narotzki/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs'
executable_firefox = '/Users/idan.narotzki/Downloads/firefox'


# continue here useing selenium to post and get results


class TabuMissim:
    url = 'https://www.misim.gov.il/svinfonadlan2010/searchGushHelka.aspx?ProcessKey=7462636c-563b-45e6-a5f5-261637d663c5'

    def __init__(self, hebrew_city):
        self.hebrew_city = hebrew_city
        self.driver = webdriver.Firefox()
        self.driver.get(TabuMissim.url)

    def execute(self, address):
        self.fill_address(address)
        search_button = self.find_search_button()
        search_button.click()
        try:
            gush, helka = self.extract_gush_helka()
            print('gush={}, helka={}'.format(gush, helka))
            return gush, helka
        except Exception as e:
            logger.warning('could NOT find gush,helka for address={}'.format(address + ' ' + self.hebrew_city))
            return 1, 1


driver = webdriver.Firefox()
driver.get(TabuMissim.url)

city = 'חיפה'
street = 'קרן היסוד'

# find_search_button
search_button = driver.find_element_by_id('ContentUsersPage_btnSearch1')
assert (search_button.get_attribute('type') == 'submit')
assert (search_button.get_attribute('value') == 'חיפוש')

# City
city_text_box = driver.find_element_by_id('ContentUsersPage_city')
assert (city_text_box.get_attribute('class') == 'hebrew ui-autocomplete-input')
city_text_box.send_keys(city)
sleep(0.5)
city_text_box.send_keys(Keys.TAB)

# street
street_text_box = driver.find_element_by_id('ContentUsersPage_rehov')
assert (street_text_box.get_attribute('class') == 'aspNetDisabled ui-autocomplete-input')
street_text_box.send_keys(street)
sleep(0.5)
street_text_box.send_keys(Keys.TAB)

# number
street_number_text_box = driver.find_element_by_id('txtBayta')
assert street_number_text_box.get_attribute('maxlength').isdigit()
street_number_text_box.send_keys(10)

search_button.click()

starting_gush, starting_helka, end_gush, end_helka = driver.find_element_by_class_name('BoxC').text.split()
print(starting_gush, starting_helka, end_gush, end_helka)

# WebDriverWait(city_text_box,5).until(lambda driver :
#         driver.find_elements_by_xpath(
#             r"//ul[@id='ui-id-1']/li"
#             )
#     )
# #after ajax complete, simulate click operation
# city_text_box.find_element_by_xpath("//ul[@id='ui-id-1']/li[1]/a").click()
