import logging
import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)


class Mapi:
    mapi_url = 'https://www.mapi.gov.il/Pages/LotAddressLocator.aspx'

    def __init__(self, hebrew_city):
        self.hebrew_city = hebrew_city
        self.driver = webdriver.Firefox()
        self.driver.get(Mapi.mapi_url)

    def fill_address(self, address):
        address = address + ' ' + self.hebrew_city
        inputbox = self.driver.find_element_by_id('AddressInput')
        logger.debug(inputbox.get_attribute('value'))  # get the typed text
        inputbox.clear()
        # displayed = inputbox.is_displayed()
        # enabled = inputbox.is_enabled()

        try:
            inputbox.send_keys(address)
        except:
            logger.exception('error sending keys with address: {}'.format(address))
            raise

    def find_search_button(self):
        links = self.driver.find_elements(By.TAG_NAME, 'a')
        logger.debug("links={}".format(len(links)))
        search_button = None
        for link in links:
            if link.text == "חפש":
                search_button = link
                break
        return search_button

    def extract_gush_helka(self):
        result_class_name = self.driver.find_elements(By.CLASS_NAME, 'Result')
        assert len(result_class_name) == 2
        logger.debug(result_class_name)
        tabu_location = None
        for result in result_class_name:
            if result.text != '':
                assert ('תוצאה' in result.text)
                for num_trials in range(3):
                    print('loop#={}'.format(num_trials))
                    if ('גוש' in result.text):
                        break
                    elif ('לא נמצא ערך' in result.text):
                        raise Exception('לא נמצא ערך')
                    sleep(2)
                assert ('גוש' in result.text)
                tabu_location = result.find_element(By.TAG_NAME, 'span').text
                assert ('תוצאה' not in tabu_location)
                assert ('גוש' in tabu_location)
                print(tabu_location)
        splitted_tabu_location = tabu_location.split(', ')
        assert len(splitted_tabu_location) == 2
        gush = splitted_tabu_location[0].replace('גוש ', '')
        helka = splitted_tabu_location[1].replace('חלקה ', '')
        return gush, helka

    def execute(self, address):
        self.fill_address(address)
        search_button = self.find_search_button()
        search_button.click()
        try:
            gush, helka = self.extract_gush_helka()
            print('gush={}, helka={}'.format(gush, helka))
            return gush, helka
        except Exception as e:
            logger.warning('could not find gush,helka in MAPI for address={}'.format(address + ' ' + self.hebrew_city))
            return 1, 1

# mapi = Mapi('חיפה')
# mapi.extract_deals_records_list_for_tabu('הראל 10 חיפה')
