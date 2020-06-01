import logging
import os

from selenium import webdriver
from selenium.webdriver.common.by import By

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

mapi_url = 'https://www.mapi.gov.il/Pages/LotAddressLocator.aspx'
executable_path_phantomjs = '/Users/idan.narotzki/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs'
executable_firefox = '/Users/idan.narotzki/Downloads/firefox'

# example 1 #

"""driver = webdriver.Firefox()
driver.get("http://pythonscraping.com/pages/javascript/ajaxDemo.html")
time.sleep(3)
print(driver.find_element_by_id("content").text)
driver.close()
"""

# example 2 #

"""def waitForLoad(driver):
    elem = driver.find_element_by_tag_name("html")
    count = 0
    while True:
        count += 1
        if count > 20:
            print("Timing out after 10 seconds and returning")
            return
        time.sleep(.5)
        try:
            elem == driver.find_element_by_tag_name("html")
        except StaleElementReferenceException:
            return


driver = webdriver.PhantomJS(executable_path=executable_path_phantomjs)
driver.get("http://pythonscraping.com/pages/javascript/redirectDemo1.html")
inputbox=driver.find_element_by_class_name('AddressInput')
waitForLoad(driver)
print(driver.page_source)"""


def main():
    driver = webdriver.Firefox()
    driver.get(mapi_url)

    def fill_address(driver, address):
        inputbox = driver.find_element_by_id('AddressInput')
        displayed = inputbox.is_displayed()
        enabled = inputbox.is_enabled()
        print(displayed, enabled)
        print(inputbox)
        try:
            inputbox.send_keys(address)
        except:
            logger.exception('error sending keys with address: {}'.format(address))
            raise

    def find_search_button():
        links = driver.find_elements(By.TAG_NAME, 'a')
        print("links={}".format(len(links)))
        search_button = None
        for link in links:
            if link.text == "חפש":
                search_button = link
                break
        return search_button

    fill_address(driver, 'קרן היסוד 10 חיפה')
    search_button = find_search_button()
    search_button.click()

    def extract_gush_helka(driver):
        result_class_name = driver.find_elements(By.CLASS_NAME, 'Result')
        assert len(result_class_name) == 2
        logger.debug(result_class_name)
        tabu_location = None
        for result in result_class_name:
            if result.text != '':
                assert ('תוצאה' in result.text)
                for num_trials in range(5):
                    print('loop#={}'.format(num_trials))
                    if ('גוש' in result.text):
                        break
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

    gush, helka = extract_gush_helka(driver)
    logger.info('gush={}, helka={}'.format(gush, helka))


if "main" == __name__:
    main()
