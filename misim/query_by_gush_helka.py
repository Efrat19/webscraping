import logging
import os
from time import sleep

from PIL import Image
from selenium import webdriver
from selenium.webdriver.support.select import Select

from misim.analyze_missim_results import AnalyzeDealsHistoryPage
from misim.captcha_images.decipher_captcha import extract_captcha_from_processed_img

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

executable_path_phantomjs = '/Users/idan.narotzki/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs'
executable_firefox = '/Users/idan.narotzki/Downloads/firefox'

url = 'https://www.misim.gov.il/svinfonadlan2010/startpageNadlanNewDesign.aspx?ProcessKey=3e778b47-d2ae-4546-a992-fa50cb00663b'
WINDOW_WIDTH = 1440
WINDOW_LENGTH = 900
ORIGINAL_CAPTCHA_IMG_PATH = '/Users/idan.narotzki/PycharmProjects/webscraping/misim/captcha_images/screenshot_original.png'
PROCESSED_CAPTCHA_PATH = '/Users/idan.narotzki/PycharmProjects/webscraping/misim/captcha_images/screenshot_processed.png'

HISTORY_PERIOD = 36


class MissimDetailsWebPages:
    url = 'https://www.misim.gov.il/svinfonadlan2010/startpageNadlanNewDesign.aspx?ProcessKey=3e778b47-d2ae-4546-a992-fa50cb00663b'

    def __init__(self, hebrew_city):
        self.hebrew_city = hebrew_city
        self.analyze_deal_history = AnalyzeDealsHistoryPage()

        self.driver = webdriver.Firefox()
        self.driver.set_window_position(0, 0)
        self.driver.set_window_size(WINDOW_WIDTH, WINDOW_LENGTH)

        self.driver.get(self.url)

    def find_search_button(self):
        search_button = self.driver.find_element_by_id('ContentUsersPage_btnHipus')
        assert search_button.get_attribute('value') == 'חיפוש'
        return search_button

    def fill_start_gush(self, start_gush_num):
        started_gush = self.driver.find_element_by_id('txtmegusha')
        assert started_gush.get_attribute('maxlength').isdigit()
        started_gush.send_keys(start_gush_num)

    def fill_end_gush(self, end_gush_num):
        end_gush = self.driver.find_element_by_id('txtadGush')
        assert end_gush.get_attribute('maxlength').isdigit()
        end_gush.send_keys(end_gush_num)

    def fill_start_helka(self, start_helka_num):
        started_helka = self.driver.find_element_by_id('txthelka')
        assert started_helka.get_attribute('maxlength').isdigit()
        started_helka.send_keys(start_helka_num)

    def fill_end_helka(self, end_helka_num):
        end_helka = self.driver.find_element_by_id('txtadHelka')
        assert end_helka.get_attribute('maxlength').isdigit()
        end_helka.send_keys(end_helka_num)

    def fill_gush_helka(self, start_gush_num, end_gush_num, start_helka_num, end_helka_num):
        # radio button
        radioElement = self.driver.find_element_by_id("rbMegush")
        assert radioElement.get_attribute("type") == "radio"
        radioElement.click()
        assert radioElement.is_selected()

        self.fill_start_gush(start_gush_num)
        self.fill_end_gush(end_gush_num)
        self.fill_start_helka(start_helka_num)
        self.fill_end_helka(end_helka_num)

    def select_deal_metadata(self, period_num):
        assert period_num in [3, 6, 12, 36]
        asset_purpose_select = Select(self.driver.find_element_by_id('ContentUsersPage_DDLTypeNehes'))
        asset_purpose_select.select_by_visible_text('דירת מגורים')

        select = Select(self.driver.find_element_by_id('ContentUsersPage_DDLMahutIska'))
        select.select_by_visible_text('דירה בבית קומות')

        select = Select(self.driver.find_element_by_id('ContentUsersPage_DDLDateType'))
        select.select_by_visible_text('ב-{} החודשים האחרונים'.format(period_num))

    def download_captcha_img(self, path_to_download_captcha_pic, path_to_processed_captcha_pic):
        # look for captcha
        captcha_img = self.driver.find_element_by_id('ContentUsersPage_RadCaptcha1_CaptchaImageUP')
        captcha_link = captcha_img.get_attribute('src')
        print('captcha_link={}'.format(captcha_link))
        sleep(1)
        self.driver.get(captcha_link)
        self.driver.save_screenshot(path_to_download_captcha_pic)
        img = self.driver.find_element_by_tag_name('img')
        print("img={}".format(img))
        location = img.location
        size = img.size
        print("img.location={}, size= {}".format(location, size))
        left = (location['x'])
        top = (location['y'])
        right = location['x'] + size['width']
        bottom1 = location['y'] + size['height']
        print("left, top, right, bottom1={}".format((left, top, right, bottom1)))
        im = Image.open(path_to_download_captcha_pic)
        LEFT = 1275
        UPPER = 780
        RIGHT = 1620
        LOWER = 870
        area = (LEFT, UPPER, RIGHT, LOWER)
        im = im.crop(area)
        im.save(path_to_processed_captcha_pic)
        self.driver.back()

    def fill_captcha_text_box(self, captcha):
        captcha_text_box = self.driver.find_element_by_id('ContentUsersPage_RadCaptcha1_CaptchaTextBox')
        assert captcha_text_box.get_attribute('maxlength') == '4'
        captcha_text_box.send_keys(captcha)

    def is_alarm_raise_from_click_search(self, end_gush, end_helka, start_gush, start_helka):
        try:
            healine = self.driver.find_element_by_id('ContentUsersPage_koteretNadlan')
            if 'הצגת מידע' in healine.text:
                print('found results successfully!')
        except Exception as e:
            try:
                alert = self.driver.find_element_by_id('ContentUsersPage_LblAlert')
                if 'לא נמצאו נתונים לחתך המבוקש' in alert.text:
                    logger.warning(
                        'Could not found data for asked gush helka {}-{}-{}-{}'.format(start_gush, end_gush,
                                                                                       start_helka,
                                                                                       end_helka))
                    return True
                else:
                    logger.error(alert.text)
            except Exception as e:
                raise e
        return False

    def extract_deals_records_list_for_tabu(self, start_gush, end_gush, start_helka, end_helka):
        self.execute_query_in_webpage(end_gush, end_helka, start_gush, start_helka)
        deals_record_list_for_tabu = []
        if not self.is_alarm_raise_from_click_search(end_gush, end_helka, start_gush, start_helka):
            deals_record_list_for_tabu = self.analyze_deal_history.extract_results(self.driver)
        return deals_record_list_for_tabu

    def execute_query_in_webpage(self, end_gush, end_helka, start_gush, start_helka):
        self.download_captcha_img(ORIGINAL_CAPTCHA_IMG_PATH, PROCESSED_CAPTCHA_PATH)
        self.fill_gush_helka(start_gush, end_gush, start_helka, end_helka)
        self.select_deal_metadata(HISTORY_PERIOD)  #
        captcha = extract_captcha_from_processed_img(PROCESSED_CAPTCHA_PATH)
        self.fill_captcha_text_box(captcha)
        sleep(0.5)
        search_button = self.find_search_button()
        search_button.click()
        sleep(1)

#
# m = MissimDetailsWebPages('חיפה')
# m.extract_deals_records_list_for_tabu(start_gush='10861', end_gush='10861', start_helka='238', end_helka='239')
