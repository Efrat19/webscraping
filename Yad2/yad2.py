import logging
import os
import re
from collections import defaultdict
from urllib.error import HTTPError
from urllib.request import urlopen

from bs4 import BeautifulSoup as soup

from Yad2.helper import hasNumbers
from Yad2.sqlite import CityRecordsSqlite

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)
YAD2_URL_PREFIX = 'https://www.yad2.co.il'

sqlite = CityRecordsSqlite('haifa', path='/Users/idan.narotzki/PycharmProjects/webscraping/Yad2')
staring_page = 118

class WebScrapper:

    def __init__(self, url):
        self.page_soup = self.get_page_soup(url)

    def get_page_soup(self, url):
        try:
            page_html = self.get_url_open(url)
        except HTTPError as e:
            print(e)
        else:
            if page_html is None:
                print("URL is not found")
            return soup(page_html, "html.parser")  # html parsing

    @staticmethod
    def get_url_open(url):
        uClient = urlopen(url)
        page_html = uClient.read()
        uClient.close()
        return page_html


class Yad2page:
    HAIFA = '4000'
    base_url = 'https://www.yad2.co.il/realestate/forsale?city={}&page=118'  # starting from 1

    def __init__(self, city):
        self.current_page_url = self.base_url.format(city)
        self.scrapper = WebScrapper(self.current_page_url)
        self.page_num = 1
        self.page_row_info_dict = defaultdict(set)

    @staticmethod
    def extract_right_col_price_from_feed_item(feed_item):

        right_col_div_list = feed_item.find_all('div', {"class": "right_col"})
        assert len(right_col_div_list) == 1
        right_col_div = right_col_div_list[0]
        # get address
        rows = right_col_div.find_all('div', {"class": "rows"})  # print (rows)
        assert len(rows) == 1
        row = rows[0]
        address = row.find('span', {'class': 'title'}).get_text()
        clean_address = address.rstrip().strip()

        if hasNumbers(clean_address):
            return clean_address
        else:
            logger.warning('address={} doesnt have number'.format(clean_address))
            return None

    @staticmethod
    def extract_room_floor_size_from_feed_item(feed_item):
        middle_col_div_list = feed_item.find_all('div', {"class": "middle_col"})
        assert len(middle_col_div_list) == 1
        middle_col_div = middle_col_div_list[0]

        rooms_num = middle_col_div.find('span', {'id': re.compile('data_rooms_[0-9]*')}).get_text()
        floor_num = middle_col_div.find('span', {'id': re.compile('data_floor_[0-9]*')}).get_text()
        square_meter = middle_col_div.find('span', {'id': re.compile('data_SquareMeter[0-9]*')}).get_text()

        if floor_num == 'קרקע':
            floor_num = '0 '

        element_list = [rooms_num, square_meter]
        print(element_list)
        for i in range(len(element_list)):
            if not hasNumbers(element_list[i]):
                logger.warning('element[{}]={} is not valid'.format(i, element_list[i]))
                element_list[i] = None

        return rooms_num, floor_num, square_meter

    @staticmethod
    def extract_left_col_price_from_feed_item(feed_item):
        left_col_div_list = feed_item.find_all('div', {'class': "left_col"})  # consider regex
        assert len(left_col_div_list) == 1
        left_col_div = left_col_div_list[0]
        dirty_price_list = left_col_div.find_all("div",
                                                 {'class': 'price'})  # '\n                1,579,000 ₪\n            '
        assert len(dirty_price_list) == 1
        dirty_price = dirty_price_list[0]
        dirty_price_text = dirty_price.get_text()
        clean_price = dirty_price_text.strip().replace('₪', '').rstrip().replace(',', '')

        if not hasNumbers(clean_price):
            logger.warning("price is not valid! price={}".format(clean_price))
            return None

        return clean_price

    def extract_yellow_feed_items_for_page(self, page_soup):

        feed_items_tables = page_soup.find_all("div", {"class": "feeditem table"})
        for feed_item in feed_items_tables:
            # right column
            address = self.extract_right_col_price_from_feed_item(feed_item)

            # center column
            rooms_num, floor_num, square_meter = self.extract_room_floor_size_from_feed_item(feed_item)

            # left column
            price = self.extract_left_col_price_from_feed_item(feed_item)

            row_info = RowInfo(address, rooms_num, floor_num, square_meter, price)

            print("adding row_info={} to self.page_row_info_dict".format(row_info.__dict__))
            self.page_row_info_dict[self.page_num].add(row_info)

        print("#feed_item_table={}".format(len(feed_items_tables)))

    def sets_for_next_page(self):
        new_url = self.get_yad2_next_page_url(self.scrapper.page_soup)
        print("set new_url={}".format(new_url))
        self.current_page_url = new_url
        self.scrapper.page_soup = self.scrapper.get_page_soup(new_url)
        self.page_num += 1

    @staticmethod
    def does_have_next_page(page_soup):
        next_button_list = page_soup.find_all('', {
            'class': 'internalLink no-button pagination-nav next nuxt-link-exact-active nuxt-link-active disabled'})
        if len(next_button_list) > 0:
            assert (len(next_button_list) == 1)
            next_button = next_button_list[0]
            if 'disabled' in next_button.get('class')[-1]:
                return False
        return True

    def get_yad2_next_page_url(self, page_soup):
        next_page_text_list = page_soup.find_all('span', {'class': 'navigation-button-text next-text'})
        assert len(next_page_text_list) == 1
        next_page_text = next_page_text_list[0]
        assert next_page_text.get_text() == 'הבא'
        next_page_text_parent = next_page_text.parent
        href_attr_list = next_page_text_parent.get_attribute_list('href')
        assert len(href_attr_list) == 1
        href_attr = href_attr_list[0]
        next_page_suffix = href_attr
        return YAD2_URL_PREFIX + next_page_suffix


class RowInfo:

    def __init__(self, address, rooms, floor_num, size, price):
        self._address = address
        self._rooms = rooms
        self._floor_num = floor_num
        self._size = size
        self._price = price

    def __repr__(self):
        return str(self.__dict__)

    @staticmethod
    def row_validator(address, rooms, floor_num, size, price):
        pass

    @property
    def address(self):
        return self._address

    @property
    def rooms(self):
        return self._rooms

    @property
    def floor_num(self):
        return self._floor_num

    @property
    def size(self):
        return self._size

    @property
    def price(self):
        return self._price

    @address.setter
    def address(self, address):
        self._address = address

    @rooms.setter
    def rooms(self, rooms):
        self._rooms = rooms

    @floor_num.setter
    def floor_num(self, size):
        self._size = size

    @price.setter
    def price(self, price):
        self._price = price


def insert_rows_info_page_to_sqlite(yad2):
    row_info_list = yad2.page_row_info_dict[yad2.page_num]
    print("working on pag_num={}".format(yad2.page_num))

    # using filter function
    rows_info_with_missing_data = set(filter(lambda row_info: None in row_info.__dict__.values(), row_info_list))
    print('out of total of {}, {} had missing data '.format(len(row_info_list), len(rows_info_with_missing_data)))
    for row_info_with_missing_data in rows_info_with_missing_data:
        logger.debug(row_info_with_missing_data)

    rows_info_with_all_needed_data = row_info_list - rows_info_with_missing_data
    print('len(rows_info_with_all_needed_data)={}'.format(len(rows_info_with_all_needed_data)))

    for complete_row_info in rows_info_with_all_needed_data:
        print('inserting the following complete_work_info dict:{}'.format(complete_row_info))
        sqlite.insert(complete_row_info)


def main():
    yad2 = Yad2page(Yad2page.HAIFA)
    print("yad2.current_page_url={}".format(yad2.current_page_url))

    yad2.extract_yellow_feed_items_for_page(yad2.scrapper.page_soup)
    insert_rows_info_page_to_sqlite(yad2)

    while yad2.does_have_next_page(yad2.scrapper.page_soup):
        yad2.sets_for_next_page()
        yad2.extract_yellow_feed_items_for_page(yad2.scrapper.page_soup)
        insert_rows_info_page_to_sqlite(yad2)

    # print(v.__dict__ for v in yad2.page_row_info_dict.values())
    # yad2 = WebScrapper(yad2.current_page_url)
    # get_yad2_next_page(yad2.page_soup)
    # next_page_url = get_yad2_next_page(yad2.page_soup)
    # yad2.set_new_url_and_page_soup(next_page_url)


if __name__ == '__main__':
    main()
