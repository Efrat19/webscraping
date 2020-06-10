import logging
import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.support.select import Select

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

executable_path_phantomjs = '/Users/idan.narotzki/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs'
executable_firefox = '/Users/idan.narotzki/Downloads/firefox'

url = 'https://www.misim.gov.il/svinfonadlan2010/startpageNadlanNewDesign.aspx?ProcessKey=3e778b47-d2ae-4546-a992-fa50cb00663b'


class MissimDetails:
    url = 'https://www.misim.gov.il/svinfonadlan2010/startpageNadlanNewDesign.aspx?ProcessKey=3e778b47-d2ae-4546-a992-fa50cb00663b'

    def __init__(self, hebrew_city):
        self.hebrew_city = hebrew_city
        self.driver = webdriver.Firefox()
        self.driver.get(self.url)

    def find_search_button(self):
        search_button = m.driver.find_element_by_id('ContentUsersPage_btnHipus')
        assert search_button.get_attribute('value') == 'חיפוש'
        return search_button

    def fill_start_gush(self, start_gush_num):
        started_gush = m.driver.find_element_by_id('txtmegusha')
        assert started_gush.get_attribute('maxlength').isdigit()
        started_gush.send_keys(start_gush_num)

    def fill_end_gush(self, end_gush_num):
        end_gush = m.driver.find_element_by_id('txtadGush')
        assert end_gush.get_attribute('maxlength').isdigit()
        end_gush.send_keys(end_gush_num)

    def fill_start_helka(self, start_helka_num):
        started_helka = m.driver.find_element_by_id('txthelka')
        assert started_helka.get_attribute('maxlength').isdigit()
        started_helka.send_keys(start_helka_num)

    def fill_end_helka(self, end_helka_num):
        end_helka = m.driver.find_element_by_id('txtadHelka')
        assert end_helka.get_attribute('maxlength').isdigit()
        end_helka.send_keys(end_helka_num)

    def fill_gush_helka(self, start_gush_num, end_gush_num, start_helka_num, end_helka_num):
        # radio button
        radioElement = m.driver.find_element_by_id("rbMegush")
        assert radioElement.get_attribute("type") == "radio"
        radioElement.click()
        assert radioElement.is_selected()

        self.fill_start_gush(start_gush_num)
        self.fill_end_gush(end_gush_num)
        self.fill_start_helka(start_helka_num)
        self.fill_end_helka(end_helka_num)

    def select_deal_metadata(self):
        asset_purpose_select = Select(m.driver.find_element_by_id('ContentUsersPage_DDLTypeNehes'))
        asset_purpose_select.select_by_visible_text('דירת מגורים')

        select = Select(m.driver.find_element_by_id('ContentUsersPage_DDLMahutIska'))
        select.select_by_visible_text('דירה בבית קומות')

        select = Select(m.driver.find_element_by_id('ContentUsersPage_DDLDateType'))
        select.select_by_visible_text('ב-6 החודשים האחרונים')

    def execute(self, start_gush, end_gush, start_helka, end_helka):
        search_button = self.find_search_button()
        self.fill_gush_helka(start_gush, end_gush, start_helka, end_helka)
        self.select_deal_metadata()
        # search_button.click()
        sleep(0.5)

        # Check if we got alert for not found
        try:
            m.driver.find_element_by_id('ContentUsersPage_LblAlert')
        except Exception as e:
            if 'Unable to locate element' in str(e):
                logger.warning(e)
            else:
                raise


m = MissimDetails('חיפה')

m.execute('1000', '1000', '80', '80')

# find search button
search_button = m.driver.find_element_by_id('ContentUsersPage_btnHipus')
assert search_button.get_attribute('value') == 'חיפוש'

# radio button
radioElement = m.driver.find_element_by_id("rbMegush")
assert radioElement.get_attribute("type") == "radio"
radioElement.click()
assert radioElement.is_selected()

# gushim
started_gush = m.driver.find_element_by_id('txtmegusha')
assert started_gush.get_attribute('maxlength').isdigit()
started_gush.send_keys('1000')

end_gush = m.driver.find_element_by_id('txtadGush')
assert end_gush.get_attribute('maxlength').isdigit()
end_gush.send_keys('1000')

started_helka = m.driver.find_element_by_id('txthelka')
assert started_helka.get_attribute('maxlength').isdigit()
started_helka.send_keys('80')

end_helka = m.driver.find_element_by_id('txtadHelka')
assert end_helka.get_attribute('maxlength').isdigit()
end_helka.send_keys('80')

# asset metadata details
asset_purpose_select = Select(m.driver.find_element_by_id('ContentUsersPage_DDLTypeNehes'))
asset_purpose_select.select_by_visible_text('דירת מגורים')

select = Select(m.driver.find_element_by_id('ContentUsersPage_DDLMahutIska'))
select.select_by_visible_text('דירה בבית קומות')

select = Select(m.driver.find_element_by_id('ContentUsersPage_DDLDateType'))
select.select_by_visible_text('ב-6 החודשים האחרונים')

# search_button.click()
