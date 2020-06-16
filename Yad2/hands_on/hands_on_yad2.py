from Yad2.yad2 import Yad2page

yad2 = Yad2page(Yad2page.HAIFA_YAD2_CODE)
print("yad2.current_page_url={}".format(yad2.current_page_url))

yad2.extract_white_yellow_and_red_feed_items_for_page(yad2.scrapper.page_soup)
yad2.sets_for_next_page()
