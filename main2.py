# fill yad2 DB for city #


# select record by record from the city #

# for each record (have record, gush, helka)

# 1. Go to Missim and get results  - 36 months and only then filter all data
# 2. Create new yad2_for_sale_properties_sqlite or edit yad2_for_sale_properties_sqlite with the results
# a. id, (address, gush, helka) - search index


# 1. Select all in yad2_table
from db.sqlite import MissimPropertiesHistory

missim_property_db = MissimPropertiesHistory('haifa', path='')

deal_record = {'gush_helka': '010861-0199-006-00', 'date_of_sale': '21/01/2019', 'declared_value': 620000.0,
               'sale_value': 620000.0, 'deal_type': 'דירה בבית קומות', 'ground_ratio': 1.0, 'city': 'חיפה',
               'built_year': '1930',
               'size': '47', 'rooms_num': '2'}

# Todo check the following
# missim_property_db.insert(deal_record, 'address')
