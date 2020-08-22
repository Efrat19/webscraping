from datetime import datetime
from sqlite3 import OperationalError
from time import sleep

from dateutil.relativedelta import relativedelta

from db.sqlite import ForSalePropertiesSqlite, MissimPropertiesHistory
from misim.query_by_gush_helka import MissimDetailsWebPages
from utils import calculate_percentile_for_property, NoRelevantHistroyPropetiesExc

LAST_NUM_MONTHS = 36
datetime_obj_months_ago = datetime.today() + relativedelta(months=-LAST_NUM_MONTHS)

yad2_for_sale_properties_sqlite = ForSalePropertiesSqlite('haifa',
                                                          path='/Users/idan.narotzki/PycharmProjects/webscraping/Yad2')
missim_prop_db = MissimPropertiesHistory('haifa', '.')
missim_webpage = MissimDetailsWebPages('חיפה')
yad2_all_rows = yad2_for_sale_properties_sqlite.select_all()

for yad2_row in yad2_all_rows:
    address = yad2_row['address']
    gush = yad2_row['gush']
    helka = yad2_row['helka']
    yad2_prop_price = float(yad2_row['price'])
    yad2_prop_size = float(yad2_row['size'])

    if yad2_row['compare_average'] == -100:
        print(f'skipping address: {address} since it saved already in the db')
        continue
    elif not yad2_row['compare_average']:

        deals_record_list_for_tabu = missim_webpage.extract_deals_records_list_for_tabu(start_gush=gush, end_gush=gush,
                                                                                        start_helka=helka,
                                                                                        end_helka=helka)

        print(f'for address {address} got the following deals_record_list_for_tabu: {deals_record_list_for_tabu}')

        relevant_records_for_average = []
        for deal_record in deals_record_list_for_tabu:
            missim_prop_db.insert(deal_record, address)

            date_time_obj = datetime.strptime(deal_record.date_of_sale, '%d/%m/%Y')
            if date_time_obj >= datetime_obj_months_ago:
                relevant_records_for_average.append(deal_record)

        try:
            yad2_prop_percentile = calculate_percentile_for_property(yad2_prop_price, yad2_prop_size,
                                                                     relevant_records_for_average, address)
            yad2_for_sale_properties_sqlite.update_average(yad2_row, yad2_prop_percentile)
        except NoRelevantHistroyPropetiesExc as e:
            print(f'{str(e)}')
            try:
                yad2_for_sale_properties_sqlite.update_average(yad2_row, -100)
            except OperationalError as e:
                print(f'{e}')




    missim_webpage.driver.back()
    missim_webpage.driver.refresh()
    sleep(2)

    # deals_record_list_for_tabu = [
    #     {'gush_helka': '010861-0199-006-00', 'date_of_sale': '21/01/2019', 'declared_value': 620000.0,
    #      'sale_value': 620000.0, 'deal_type': 'דירה בבית קומות', 'ground_ratio': 1.0, 'city': 'חיפה',
    #      'built_year': '1930', 'size': '47', 'rooms_num': '2'}]
