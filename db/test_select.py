from misim.analyze_missim_results import DealsRecords

first_row = {'id': 1, 'address': 'אלתר 6', 'rooms': 4.0, 'floor_num': 2.0, 'size': 90.0, 'price': 1500000.0,
             'created_at': '2020-06-16 22:37:18', 'updated_at': '2020-06-16 22:37:18', 'gush': '11879', 'helka': '18',
             'compare_average': None, 'was_fixed': None}

deal_records_example = {'gush_helka': '010861-0238-003-00', 'date_of_sale': '12/09/2019', 'declared_value': '510000.0',
                        'sale_value': '510000.0', 'deal_type': 'דירה בבית קומות', 'ground_ratio': 1.0, 'city': 'חיפה',
                        'built_year': '1970', 'size': '46', 'rooms_num': '3'}

deal_records = DealsRecords(**deal_records_example)
print(deal_records_example)
