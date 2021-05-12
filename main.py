# -*- coding: utf-8 -*- 
from datetime import datetime
from sqlite3 import OperationalError
from time import sleep

from dateutil.relativedelta import relativedelta

from db.sqlite import ForSalePropertiesSqlite, MissimPropertiesHistory
from misim.query_by_gush_helka import MissimDetailsWebPages
from utils import calculate_percentile_for_property, NoRelevantHistoryPropertiesExc

LAST_NUM_MONTHS = 36
datetime_obj_months_ago = datetime.today() + relativedelta(months=-LAST_NUM_MONTHS)

yad2_for_sale_properties_sqlite = ForSalePropertiesSqlite('haifa',
                                                          path='/Users/idan.narotzki/PycharmProjects/webscraping/Yad2')
missim_prop_db = MissimPropertiesHistory('haifa', '.')
missim_webpage = MissimDetailsWebPages('חיפה')


def select_yad2_rows_and_update_avg():
    yad2_rows_with_no_avg = yad2_for_sale_properties_sqlite.select_all_with_no_avg()

    for yad2_row in yad2_rows_with_no_avg:
        deals_record_list_for_tabu = missim_webpage.extract_deals_records_list_for_tabu(start_gush=yad2_row['gush'],
                                                                                        end_gush=yad2_row['gush'],
                                                                                        start_helka=yad2_row['helka'],
                                                                                        end_helka=yad2_row['helka'])

        print('for address {yad2_row["address"]} got the following deals_record_list_for_tabu: '%deals_record_list_for_tabu)

        relevant_records_for_average = []
        update_avg_for_yad2_row_in_db(yad2_row, deals_record_list_for_tabu, relevant_records_for_average)

        refresh_web_page_actions()


def update_avg_for_yad2_row_in_db(yad2_row, deals_record_list_for_tabu, relevant_records_for_average):
    for deal_record in deals_record_list_for_tabu:
        missim_prop_db.insert(deal_record, yad2_row["address"])

        date_time_obj = datetime.strptime(deal_record.date_of_sale, '%d/%m/%Y')
        if date_time_obj >= datetime_obj_months_ago:
            relevant_records_for_average.append(deal_record)
    try:
        yad2_prop_percentile = calculate_percentile_for_property(yad2_row, relevant_records_for_average)
        yad2_for_sale_properties_sqlite.update_average(yad2_row, yad2_prop_percentile)
    except NoRelevantHistoryPropertiesExc as e:
        print('{str(e)}')
        try:
            yad2_for_sale_properties_sqlite.update_average(yad2_row, -100)
        except OperationalError as e:
            print('{e}')


def refresh_web_page_actions():
    missim_webpage.driver.back()
    missim_webpage.driver.refresh()
    sleep(2)


if __name__ == '__main__':
    select_yad2_rows_and_update_avg()
