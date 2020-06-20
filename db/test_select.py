from db.sqlite import CityRecordsSqlite

sqlite = CityRecordsSqlite('haifa', path='/Users/idan.narotzki/PycharmProjects/webscraping/Yad2')
sqlite.select_address_and_print('יצחק שדה 35')
