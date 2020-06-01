import logging
import os
import re
from urllib.error import HTTPError
from urllib.request import urlopen

from bs4 import BeautifulSoup as soup

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)
YAD2_URL_PREFIX = 'https://www.yad2.co.il'


class WebScrapper:

    def __init__(self, url):
        self.my_url = url
        self.page_soup = self.get_page_soup()

    def get_page_soup(self):
        try:
            page_html = self.get_url_open(self.my_url)
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

    def set_new_url_and_page_soup(self, new_url):
        print("set new_url={}".format(new_url))
        self.my_url = new_url
        self.page_soup = self.get_page_soup()


def main():
    def get_yad2_next_page(page_soup):
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

    HAIFA = '4000'
    yad2_url = "https://www.yad2.co.il/realestate/forsale?city={}&page=2".format(HAIFA)
    print(yad2_url)
    yad2 = WebScrapper(yad2_url)

    # get_yad2_next_page(yad2.page_soup)

    def extract_right_col_price_from_feed_item(feed_item):

        right_col_div_list = feed_item.find_all('div', {"class": "right_col"})
        assert len(right_col_div_list) == 1
        right_col_div = right_col_div_list[0]  # print (right_col_div, "\n")
        # get address
        rows = right_col_div.find_all('div', {"class": "rows"})  # print (rows)
        assert len(rows) == 1
        row = rows[0]
        address = row.find('span', {'class': 'title'}).get_text()
        return address.rstrip().strip()

    def extract_room_floor_size_from_feed_item(feed_item):
        middle_col_div_list = feed_item.find_all('div', {"class": "middle_col"})
        assert len(middle_col_div_list) == 1
        middle_col_div = middle_col_div_list[0]
        rooms_num = middle_col_div.find('span', {'id': re.compile('data_rooms_[0-9]*')}).get_text()
        floor_num = middle_col_div.find('span', {'id': re.compile('data_floor_[0-9]*')}).get_text()
        square_meter = middle_col_div.find('span', {'id': re.compile('data_SquareMeter[0-9]*')}).get_text()

        return rooms_num, floor_num, square_meter

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
        # check there are char
        for c in clean_price:
            if not c.isdigit():
                logger.warning("price is not valid! price={}".format(clean_price))
                return None
        return clean_price

    def print_yellow_feed_items_for_page(page_soup):
        feed_items_tables = page_soup.find_all("div", {"class": "feeditem table"})
        for feed_item in feed_items_tables:
            # right column
            address = extract_right_col_price_from_feed_item(feed_item)
            logger.info('address={}'.format(address))

            # center column
            rooms_num, floor_num, square_meter = extract_room_floor_size_from_feed_item(feed_item)
            logger.info('rooms_num={}, floor_num={}, square_meter={}'.format(rooms_num, floor_num, square_meter))

            # left column
            price = extract_left_col_price_from_feed_item(feed_item)
            logger.info(price)

            # Todo: create feed item class

        print("#feed_item_table={}".format(len(feed_items_tables)))

    print_yellow_feed_items_for_page(yad2.page_soup)

    next_page_url = get_yad2_next_page(yad2.page_soup)
    yad2.set_new_url_and_page_soup(next_page_url)

    print_yellow_feed_items_for_page(yad2.page_soup)


if __name__ == '__main__':
    main()
