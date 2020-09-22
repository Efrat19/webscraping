import logging
import os
from time import sleep

from retry import retry
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)


class TabuMissimWebPage:
    url = 'https://www.misim.gov.il/svinfonadlan2010/searchGushHelka.aspx?ProcessKey=7462636c-563b-45e6-a5f5-261637d663c5'

    def __init__(self, hebrew_city):
        self.hebrew_city = hebrew_city
        self.driver = webdriver.Firefox()
        self.driver.get(TabuMissimWebPage.url)

    def find_search_button(self):
        search_button = self.driver.find_element_by_id('ContentUsersPage_btnSearch1')
        assert (search_button.get_attribute('type') == 'submit')
        assert (search_button.get_attribute('value') == 'חיפוש')
        return search_button

    def fill_city_in_text_box_and_tab(self):
        city_text_box = self.driver.find_element_by_id('ContentUsersPage_city')
        try:
            assert (city_text_box.get_attribute('class') == 'hebrew ui-autocomplete-input')
        except:
            logger.error("could Not find city textbox to feel in ")
            raise

        city_text_box.clear()
        city_text_box.send_keys(self.hebrew_city)
        sleep(1)
        city_text_box.send_keys(Keys.TAB)

    @retry(tries=-1, delay=20, max_delay=90, backoff=1)
    def fill_street_in_text_box_and_tab(self, street):
        sleep(1)
        street_text_box = self.driver.find_element_by_id('ContentUsersPage_rehov')
        try:
            assert (street_text_box.get_attribute('class') == 'aspNetDisabled ui-autocomplete-input')
        except Exception as e:
            self.driver.refresh()
            raise e
        street_text_box.clear()
        street_text_box.send_keys(street)
        sleep(1)
        street_text_box.send_keys(Keys.TAB)

    def fill_number_text_box(self, street_num):
        street_number_text_box = self.driver.find_element_by_id('txtBayta')
        assert street_number_text_box.get_attribute('maxlength').isdigit()
        street_number_text_box.clear()
        street_number_text_box.send_keys(street_num)

    def getting_gush_helka(self, street, num):
        # todo: handle exception better
        try:
            darker_row = self.driver.find_elements_by_class_name('BoxC')
            brighter_row = self.driver.find_elements_by_class_name('BoxB')

            if len(darker_row) == 0:
                logger.error(
                    "didn't find gush helka for {} {}".format(street, num, ))
                return 2, 2

            elif len(darker_row) > 1 or len(brighter_row) > 1:
                logger.error(
                    "There is more than 1 gush helka which is relevant for {} {} in {}. taking only the first row".format(
                        street, num, self.hebrew_city))

            starting_gush, starting_helka, end_gush, end_helka = darker_row[0].text.split()
            if starting_gush != end_gush or starting_helka != end_helka:
                raise Exception('diff in gushes or helkas')
            return starting_gush, starting_helka

        except Exception as e:
            if 'Unable to locate element: .Box' in str(e):
                # check that not found for this address
                not_found_alert = self.driver.find_element_by_id('ContentUsersPage_lblAlert1')
                if 'לא נמצאו נתונים לחתך המבוקש' in not_found_alert.text:
                    logger.warning(
                        "could NOT find data for city={} street={} num={} לא נמצאו נתונים לחתך המבוקש".format(
                            self.hebrew_city, street, num))
                    return 2, 2
                elif 'סוג נכס לא תקין' in not_found_alert.text:
                    logger.warning(
                        "נכס לא תקיו could NOT find data for city={} street={} num={}".format(self.hebrew_city, street,
                                                                                              num))
                    return 2, 2

            else:
                raise

    @retry(tries=-1, delay=20, max_delay=90, backoff=1)
    def execute(self, street, num):
        try:
            search_button = self.find_search_button()
            self.fill_city_in_text_box_and_tab()
            self.fill_street_in_text_box_and_tab(street)
            self.fill_number_text_box(num)

            search_button.click()
            sleep(0.5)

            gush, helka = self.getting_gush_helka(street, num)
            self.driver.back()
        except Exception as e:
            self.driver.refresh()
            raise e
        return gush, helka

# tabu_missim_page = TabuMissim('חיפה')
