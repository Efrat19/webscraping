from Yad2.yad2 import RowInfo
from db.sqlite import ForSalePropertiesSqlite

row_info = {'ארלוזורוב 3', '3.5', '2', '110 ', '1090000'}

row_info = RowInfo('ארלוזורוב 3', '3.5', '2', '110 ', '1090000')
print((row_info.__dict__))
sqlite = ForSalePropertiesSqlite('haifa', path='/Users/idan.narotzki/PycharmProjects/webscraping/Yad2')

sqlite.insert(row_info.__dict__)
