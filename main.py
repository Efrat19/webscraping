# fill yad2 DB for city #


# select record by record from the city #

# for each record (have record, gush, helka)

# 1. Go to Missim and get results  - 36 months and only then filter all data
# 2. Create new yad2_for_sale_properties_sqlite or edit yad2_for_sale_properties_sqlite with the results
# a. id, (address, gush, helka) - search index


# 1. Select all in yad2_table
from db.sqlite import ForSalePropertiesSqlite, MissimPropertiesHistory
from misim.query_by_gush_helka import MissimDetailsWebPages

yad2_for_sale_properties_sqlite = ForSalePropertiesSqlite('haifa',
                                                          path='/Users/idan.narotzki/PycharmProjects/webscraping/Yad2')
missim_prop_db = MissimPropertiesHistory('haifa', '.')
missim_webpage = MissimDetailsWebPages('חיפה')
all_rows = yad2_for_sale_properties_sqlite.select_all()

for row in all_rows:
    address = row['address']
    rooms = row['rooms']
    floor_num = row['floor_num']
    size = row['size']
    gush = row['gush']
    helka = row['helka']

    if 'אלתר' in address:
        continue

    # 2. fill MissimPropertiesHistory table accordingly
    deals_record_list_for_tabu = missim_webpage.extract_deals_records_list_for_tabu(start_gush=gush, end_gush=gush,
                                                                                    start_helka=helka, end_helka=helka)
    print(f'for address {address} got the following deals_record_list_for_tabu: {deals_record_list_for_tabu}')

    # save to db
    deal_records = deals_record_list_for_tabu[0]
    missim_prop_db.insert(deal_records, address)
    missim_webpage.driver.back()

    # deals_record_list_for_tabu = [
    #     {'gush_helka': '010861-0199-006-00', 'date_of_sale': '21/01/2019', 'declared_value': 620000.0,
    #      'sale_value': 620000.0, 'deal_type': 'דירה בבית קומות', 'ground_ratio': 1.0, 'city': 'חיפה',
    #      'built_year': '1930', 'size': '47', 'rooms_num': '2'},
    #     {'gush_helka': '010861-0199-005-00', 'date_of_sale': '08/09/2017', 'declared_value': 624000.0,
    #      'sale_value': 624000.0, 'deal_type': 'דירה בבית קומות', 'ground_ratio': 1.0, 'city': 'חיפה',
    #      'built_year': '1930', 'size': '62', 'rooms_num': '3'},
    #     {'gush_helka': '010861-0199-007-00', 'date_of_sale': '10/04/2018', 'declared_value': 655000.0,
    #      'sale_value': 655000.0, 'deal_type': 'דירה בבית קומות', 'ground_ratio': 1.0, 'city': 'חיפה',
    #      'built_year': '1930', 'size': '62', 'rooms_num': '3'},
    #     {'gush_helka': '010861-0199-002-00', 'date_of_sale': '21/01/2019', 'declared_value': 640000.0,
    #      'sale_value': 640000.0, 'deal_type': 'דירה בבית קומות', 'ground_ratio': 1.0, 'city': 'חיפה',
    #      'built_year': '1930', 'size': '47', 'rooms_num': '2'},
    #     {'gush_helka': '010861-0199-003-00', 'date_of_sale': '19/02/2019', 'declared_value': 640000.0,
    #      'sale_value': 640000.0, 'deal_type': 'דירה בבית קומות', 'ground_ratio': 1.0, 'city': 'חיפה',
    #      'built_year': '1930', 'size': '58', 'rooms_num': '2'}]

    # sale_value vs declared vallue

    # 3. update avarage
