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
        assert (street_text_box.get_attribute('class') == 'aspNetDisabled ui-autocomplete-input')
        street_text_box.clear()
        street_text_box.send_keys(street)
        sleep(0.5)
        street_text_box.send_keys(Keys.TAB)

    def fill_number_text_box(self, street_num):
        street_number_text_box = self.driver.find_element_by_id('txtBayta')
        assert street_number_text_box.get_attribute('maxlength').isdigit()
        street_number_text_box.clear()
        street_number_text_box.send_keys(street_num)

    def getting_gush_helka(self):
        starting_gush, starting_helka, end_gush, end_helka = self.driver.find_element_by_class_name('BoxC').text.split()
        return starting_gush, starting_helka, end_gush, end_helka

    def execute(self, street, num):
        search_button = self.find_search_button()
        self.fill_city_in_text_box_and_tab()
        self.fill_street_in_text_box_and_tab(street)
        self.fill_number_text_box(num)

        search_button.click()
        sleep(0.5)

        starting_gush, starting_helka, end_gush, end_helka = self.getting_gush_helka()
        print(starting_gush, starting_helka, end_gush, end_helka)


tabu_missim = TabuMissim('חיפה')
