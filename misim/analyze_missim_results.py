import logging
import os

from selenium import webdriver

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

executable_path_phantomjs = '/Users/idan.narotzki/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs'
executable_firefox = '/Users/idan.narotzki/Downloads/firefox'

url = 'https://www.misim.gov.il/svinfonadlan2010/InfoNadlanPerutWithMap.aspx?ProcessKey=3e778b47-d2ae-4546-a992-fa50cb00663b'
deal_records_list = []


class AnalyzeDealsHistoryPage:

    def __init__(self):
        self.deals_record_list = []
        self.table_titles_order = [None, None, 'גוש חלקה', '*יום מכירה', '*תמורה מוצהרת בש"ח', '*שווי מכירה בש"ח',
                                   'מהות', 'חלק נמכר', 'ישוב', 'שנת בניה', 'שטח', 'חדרים']

    def extract_results(self, driver):
        self.validate_page_order(driver)
        num_of_rows = self.extract_num_of_table_rows(driver)

        for i in range(2, 2 + num_of_rows):
            gush_helka = driver.find_element_by_xpath(
                f'/html/body/div[2]/form/div[5]/div[3]/div[6]/div/div/table/tbody/tr[{i}]/td[2]').text
            date_of_sale = driver.find_element_by_xpath(
                f'/html/body/div[2]/form/div[5]/div[3]/div[6]/div/div/table/tbody/tr[{i}]/td[3]').text
            declared_value = driver.find_element_by_xpath(
                f'/html/body/div[2]/form/div[5]/div[3]/div[6]/div/div/table/tbody/tr[{i}]/td[4]').text
            sale_value = driver.find_element_by_xpath(
                f'/html/body/div[2]/form/div[5]/div[3]/div[6]/div/div/table/tbody/tr[{i}]/td[5]').text
            deal_type = driver.find_element_by_xpath(
                f'/html/body/div[2]/form/div[5]/div[3]/div[6]/div/div/table/tbody/tr[{i}]/td[6]').text
            ground_ratio = driver.find_element_by_xpath(
                f'/html/body/div[2]/form/div[5]/div[3]/div[6]/div/div/table/tbody/tr[{i}]/td[7]').text
            city = driver.find_element_by_xpath(
                f'/html/body/div[2]/form/div[5]/div[3]/div[6]/div/div/table/tbody/tr[{i}]/td[8]').text
            built_year = driver.find_element_by_xpath(
                f'/html/body/div[2]/form/div[5]/div[3]/div[6]/div/div/table/tbody/tr[{i}]/td[9]').text
            size = driver.find_element_by_xpath(
                f'/html/body/div[2]/form/div[5]/div[3]/div[6]/div/div/table/tbody/tr[{i}]/td[10]').text
            rooms_num = driver.find_element_by_xpath(
                f'/html/body/div[2]/form/div[5]/div[3]/div[6]/div/div/table/tbody/tr[{i}]/td[11]').text

            deal_records = DealsRecords(gush_helka, date_of_sale, declared_value, sale_value, deal_type, ground_ratio,
                                        city, built_year, size, rooms_num)
            print(deal_records)
            self.deals_record_list.append(deal_records)

        # Todo: add to DB that will be created

    def extract_num_of_table_rows(self, driver):
        rows1_type = driver.find_elements_by_class_name('row1')
        boxB_type = driver.find_elements_by_class_name('BoxB')
        num_of_rows = len(rows1_type) + len(boxB_type)
        print(f'got {num_of_rows} num of rows')
        return num_of_rows

    def validate_page_order(self, driver):
        assert \
            driver.find_elements_by_xpath(
                '/html/body/div[2]/form/div[5]/div[3]/div[6]/div/div/table/tbody/tr[1]/th[2]')[
                0].text == self.table_titles_order[2]
        assert \
            driver.find_elements_by_xpath(
                '/html/body/div[2]/form/div[5]/div[3]/div[6]/div/div/table/tbody/tr[1]/th[3]')[
                0].text == self.table_titles_order[3]
        assert \
            driver.find_elements_by_xpath(
                '/html/body/div[2]/form/div[5]/div[3]/div[6]/div/div/table/tbody/tr[1]/th[4]')[
                0].text == self.table_titles_order[4]
        assert \
            driver.find_elements_by_xpath(
                '/html/body/div[2]/form/div[5]/div[3]/div[6]/div/div/table/tbody/tr[1]/th[5]')[
                0].text == self.table_titles_order[5]
        assert \
            driver.find_elements_by_xpath(
                '/html/body/div[2]/form/div[5]/div[3]/div[6]/div/div/table/tbody/tr[1]/th[6]')[
                0].text == self.table_titles_order[6]
        assert \
            driver.find_elements_by_xpath(
                '/html/body/div[2]/form/div[5]/div[3]/div[6]/div/div/table/tbody/tr[1]/th[7]')[
                0].text == self.table_titles_order[7]
        assert \
            driver.find_elements_by_xpath(
                '/html/body/div[2]/form/div[5]/div[3]/div[6]/div/div/table/tbody/tr[1]/th[8]')[
                0].text == self.table_titles_order[8]
        assert \
            driver.find_elements_by_xpath(
                '/html/body/div[2]/form/div[5]/div[3]/div[6]/div/div/table/tbody/tr[1]/th[9]')[
                0].text == self.table_titles_order[9]
        assert \
            driver.find_elements_by_xpath(
                '/html/body/div[2]/form/div[5]/div[3]/div[6]/div/div/table/tbody/tr[1]/th[10]')[
                0].text == self.table_titles_order[10]
        assert \
            driver.find_elements_by_xpath(
                '/html/body/div[2]/form/div[5]/div[3]/div[6]/div/div/table/tbody/tr[1]/th[11]')[
                0].text == self.table_titles_order[11]

    def compare_average_by(self, yad2_record):
        # Todo: update it
        pass


class DealsRecords:

    def __init__(self, gush_helka, date_of_sale, declared_value, sale_value, deal_type, ground_ratio, city, built_year,
                 size, rooms_num):
        self.gush_helka = gush_helka
        self.date_of_sale = date_of_sale
        self.declared_value = float(declared_value.replace(',', ''))
        self.sale_value = float(sale_value.replace(',', ''))
        self.deal_type = deal_type
        self.ground_ratio = float(ground_ratio)
        self.city = city
        self.built_year = built_year
        self.size = size
        self.rooms_num = rooms_num

    def __repr__(self):
        return str(self.__dict__)


def extract_street_and_street_num(address_section_info):
    street_unfiltered = None
    street_num_unfiltered = None
    for elm in address_section_info:
        if 'רחוב' in elm:
            street_unfiltered = elm
        elif 'מספר בית' in elm:
            street_num_unfiltered = elm
    street = street_unfiltered.split(':')[-1].strip().rstrip()
    street_num = street_num_unfiltered.split(':')[-1].strip().rstrip()
    return (street, street_num)


def main():
    driver = webdriver.Firefox()
    driver.get(url)

    section_info = driver.find_element_by_id('lblInfo')
    address_section_info = section_info.text.rstrip().split('\n')[1].split(
        '  ')  # ['ישוב: חיפה', '', '', '', ' רחוב: יפה נוף', '', '', '', ' מספר בית: 111']

    city = address_section_info[0].split(':')[1].strip()
    street, street_num = extract_street_and_street_num(address_section_info)

    driver.find_elements_by_class_name('table_title')

    # rows1_type = driver.find_elements_by_class_name('row1')
    # boxB_type = driver.find_elements_by_class_name('BoxB')
    # num_of_rows = len(rows1_type) + len(boxB_type)
    #
    # for i in range(2, 2 + num_of_rows):
    #     gush_helka = driver.find_element_by_xpath(
    #         f'/html/body/div[2]/form/div[5]/div[3]/div[6]/div/div/table/tbody/tr[{i}]/td[2]').text
    #     date_of_sale = driver.find_element_by_xpath(
    #         f'/html/body/div[2]/form/div[5]/div[3]/div[6]/div/div/table/tbody/tr[{i}]/td[3]').text
    #     declared_value = driver.find_element_by_xpath(
    #         f'/html/body/div[2]/form/div[5]/div[3]/div[6]/div/div/table/tbody/tr[{i}]/td[4]').text
    #     sale_value = driver.find_element_by_xpath(
    #         f'/html/body/div[2]/form/div[5]/div[3]/div[6]/div/div/table/tbody/tr[{i}]/td[5]').text
    #     deal_type = driver.find_element_by_xpath(
    #         f'/html/body/div[2]/form/div[5]/div[3]/div[6]/div/div/table/tbody/tr[{i}]/td[6]').text
    #     ground_ratio = driver.find_element_by_xpath(
    #         f'/html/body/div[2]/form/div[5]/div[3]/div[6]/div/div/table/tbody/tr[{i}]/td[7]').text
    #     city = driver.find_element_by_xpath(
    #         f'/html/body/div[2]/form/div[5]/div[3]/div[6]/div/div/table/tbody/tr[{i}]/td[8]').text
    #     built_year = driver.find_element_by_xpath(
    #         f'/html/body/div[2]/form/div[5]/div[3]/div[6]/div/div/table/tbody/tr[{i}]/td[9]').text
    #     size = driver.find_element_by_xpath(
    #         f'/html/body/div[2]/form/div[5]/div[3]/div[6]/div/div/table/tbody/tr[{i}]/td[10]').text
    #     rooms_num = driver.find_element_by_xpath(
    #         f'/html/body/div[2]/form/div[5]/div[3]/div[6]/div/div/table/tbody/tr[{i}]/td[11]').text
    #
    #     deal_records = DealsRecords(gush_helka, date_of_sale, declared_value, sale_value, deal_type, ground_ratio, city,
    #                                 built_year, size, rooms_num)
    #     print(deal_records)
    #     deal_records_list.append(deal_records)


if __name__ == '__main__':
    main()
