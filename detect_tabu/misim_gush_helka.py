import logging
import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

executable_path_phantomjs = '/Users/idan.narotzki/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs'
executable_firefox = '/Users/idan.narotzki/Downloads/firefox'


class TabuMissim:
    url = 'https://www.misim.gov.il/svinfonadlan2010/searchGushHelka.aspx?ProcessKey=7462636c-563b-45e6-a5f5-261637d663c5'

    def __init__(self, hebrew_city):
        self.hebrew_city = hebrew_city
        self.driver = webdriver.Firefox()
        self.driver.get(TabuMissim.url)

    def find_search_button(self):
        search_button = self.driver.find_element_by_id('ContentUsersPage_btnSearch1')
        assert (search_button.get_attribute('type') == 'submit')
        assert (search_button.get_attribute('value') == 'חיפוש')
        return search_button

    def fill_city_in_text_box_and_tab(self):
        city_text_box = self.driver.find_element_by_id('ContentUsersPage_city')
        assert (city_text_box.get_attribute('class') == 'hebrew ui-autocomplete-input')
        city_text_box.clear()
        city_text_box.send_keys(self.hebrew_city)
        sleep(0.5)
        city_text_box.send_keys(Keys.TAB)

    def fill_street_in_text_box_and_tab(self, street):
        street_text_box = self.driver.find_element_by_id('ContentUsersPage_rehov')
        try:
            assert (street_text_box.get_attribute('class') == 'aspNetDisabled ui-autocomplete-input')
        except Exception:
            logger.error("street_text_box.get_attribute('class')={}".format(street_text_box.get_attribute('class')))
            raise
        street_text_box.clear()
        street_text_box.send_keys(street)
        sleep(0.5)
        street_text_box.send_keys(Keys.TAB)

    def fill_number_text_box(self, street_num):
        street_number_text_box = self.driver.find_element_by_id('txtBayta')
        assert street_number_text_box.get_attribute('maxlength').isdigit()
        street_number_text_box.clear()
        street_number_text_box.send_keys(street_num)

    def getting_gush_helka(self, street, num):
        try:
            starting_gush, starting_helka, end_gush, end_helka = self.driver.find_element_by_class_name(
                'BoxC').text.split()
            if starting_gush != end_gush or starting_helka != end_helka:
                raise Exception('diff in gushes or helkas')

        except Exception as e:
            if 'Unable to locate element: .BoxC' in str(e):
                # check that not found for this address
                not_found_alert = self.driver.find_element_by_id('ContentUsersPage_lblAlert1')
                if 'לא נמצאו נתונים לחתך המבוקש' in not_found_alert.text:
                    logger.warning(
                        "couldnot find data for city={} street={} num={}".format(self.hebrew_city, street, num))
                    return 2, 2
            else:
                raise
        else:
            return starting_gush, starting_helka

    def execute(self, street, num):
        search_button = self.find_search_button()
        self.fill_city_in_text_box_and_tab()
        self.fill_street_in_text_box_and_tab(street)
        self.fill_number_text_box(num)

        search_button.click()
        sleep(0.5)

        gush, helka = self.getting_gush_helka(street, num)
        self.driver.back()
        print(gush, helka)

        return gush, helka

# tabu_missim = TabuMissim('חיפה')
