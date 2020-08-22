import datetime
import logging
import os
import sqlite3
import sys

from misim.analyze_missim_results import DealsRecords

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)


class ForSalePropertiesSqlite(object):
    FIELDS = ['id', 'address', 'rooms', 'floor_num', 'size', 'price', 'created_at', 'updated_at', 'gush', 'helka',
              'compare_average']
    table_name = 'yad2_records'

    def __init__(self, city_name, path=None):
        print("Starting initialization of the SQLite")
        self.db_name = '{}.db'.format(city_name)
        db_path = os.path.join(path, 'sqlite_' + self.db_name)
        self.sqlite_connection = sqlite3.connect(db_path)

        sqlite_create_table_query = f'CREATE TABLE if NOT EXISTS "{self.table_name}" (' \
                                    'id INTEGER PRIMARY KEY,' \
                                    'address TEXT  NOT NULL,' \
                                    'rooms TEXT NOT NULL, ' \
                                    'floor_num TEXT NOT NULL, ' \
                                    'size TEXT NOT NULL, ' \
                                    'price TEXT NOT NULL, ' \
                                    'created_at datetime NOT NULL, ' \
                                    'updated_at datetime NOT NULL, ' \
                                    'gush TEXT NULL, ' \
                                    'helka TEXT NULL , ' \
                                    'compare_average FLOAT NULL , ' \
                                    ' UNIQUE (address, rooms, floor_num, size, price));'

        cursor = self.sqlite_connection.cursor()
        self.sqlite_connection.row_factory = sqlite3.Row
        print("Successfully Connected to SQLite")
        cursor.execute(sqlite_create_table_query)

        cursor.execute("CREATE INDEX IF NOT EXISTS row_info ON yad2_records (address, rooms, floor_num, size, price);")

        self.sqlite_connection.commit()
        print("SQLite table created")

        cursor.close()

    def insert(self, row_info, g, h):
        print('row_info={}'.format(row_info))
        cursor = self.sqlite_connection.cursor()

        now = datetime.datetime.now()
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")

        insert_query = "INSERT INTO yad2_records (address, rooms, floor_num, size, price, created_at, updated_at, gush, helka) VALUES (?, ?, ?, ?, ?, ?, ?,?,?)".format(
            self.table_name)

        try:
            cursor.execute(insert_query, (row_info.address, row_info.rooms, row_info.floor_num,
                                          row_info.size, row_info.price,
                                          now_str, now_str, g, h))
        except sqlite3.IntegrityError as e:
            print(e.__str__())
            if "UNIQUE constraint failed:" in str(e):
                logging.warning('The Record already exists in the db. record: {}, '.format(row_info))
                return 0
            raise

        if not cursor.lastrowid:
            raise Exception("Row_info {}, failed to be inserted".format(row_info))

        self.sqlite_connection.commit()
        print("Record inserted successfully")
        cursor.close()

    def select_address_and_print(self, add):
        print('selecting address={}'.format(add))
        cursor = self.sqlite_connection.cursor()

        select_query = "SELECT * FROM '{}' WHERE address='{}'".format(self.table_name, add)

        try:
            query_result = cursor.execute(select_query)
            rows = query_result.fetchall()
            n = len(rows)
            for i in range(n):
                print('match row_num={}'.format(i))
                row = rows[i]
                print('address={}'.format(row['address']))
                print('keys={}'.format(row.keys()))
                for memeber in row:
                    print('{}'.format(memeber))
                    # print ('{}={}'.format(memeber, row[memeber]))
        finally:
            cursor.close()

    def select_all(self):
        print('selecting all from yad2_for_sale_properties_sqlite')
        cursor = self.sqlite_connection.cursor()

        select_query = f"SELECT * FROM '{self.table_name}'"

        try:
            query_result = cursor.execute(select_query)
            rows = query_result.fetchall()
            n = len(rows)
            for i in range(n):
                print('match row_num={}'.format(i))
                row = rows[i]
                print('address={}'.format(row['address']))
                print('keys={}'.format(row.keys()))
                for memeber in row:
                    print('{}'.format(memeber))
                    # print ('{}={}'.format(memeber, row[memeber]))
            return rows
        finally:
            cursor.close()

    def select_all_with_no_avg(self):
        print('selecting all from yad2_for_sale_properties_sqlite')
        cursor = self.sqlite_connection.cursor()

        select_query = f"SELECT * FROM '{self.table_name}' WHERE compare_average!=0"  # check this one

        try:
            query_result = cursor.execute(select_query)
            rows = query_result.fetchall()
            n = len(rows)
            for i in range(n):
                print('match row_num={}'.format(i))
                row = rows[i]
                print('address={}'.format(row['address']))
                print('keys={}'.format(row.keys()))
                for memeber in row:
                    print('{}'.format(memeber))
                    # print ('{}={}'.format(memeber, row[memeber]))
            return rows
        finally:
            cursor.close()

    def update_average(self, yad2_row, average: float):
        cursor = self.sqlite_connection.cursor()
        query = f"UPDATE {self.table_name} SET updated_at = '{datetime.datetime.now()}', compare_average = '{average}' " \
                f"WHERE address = '{yad2_row['address']}' " \
                f"AND rooms = '{yad2_row['rooms']}' AND floor_num = '{yad2_row['floor_num']}' " \
                f"AND size = '{yad2_row['size']}' AND price = '{yad2_row['price']}'"

        cursor.execute(query)  # problem with address like ח'ורי etc
        self.sqlite_connection.commit()
        print(f'Record updated successfully with average of {average}')
        cursor.close()

    def close(self):
        print("Closing SQL connection")
        self.sqlite_connection.close()


class MissimPropertiesHistory(object):
    FIELDS = ['id', 'gush_helka', 'address',
              'date_of_sale', 'declared_value', 'sale_value', 'deal_type',
              'tabu_ratio', 'built_year', 'size', 'rooms_num', 'updated_at']
    table_name = 'missim_history_records'

    def __init__(self, city_name, path=None):
        print("Starting initialization of the SQLite")
        self.db_name = f'records_history_{city_name}.db'
        db_path = os.path.join(path, 'sqlite_' + self.db_name)
        self.sqlite_connection = sqlite3.connect(db_path)

        sqlite_create_table_query = f'CREATE TABLE if NOT EXISTS "{self.table_name}" (' \
                                    'id INTEGER PRIMARY KEY,' \
                                    'gush_helka TEXT NOT NULL,' \
                                    'address TEXT  NOT NULL,' \
                                    'date_of_sale TEXT  NOT NULL,' \
                                    'declared_value FLOAT NOT NULL,' \
                                    'sale_value FLOAT NOT NULL,' \
                                    'deal_type TEXT NOT NULL,' \
                                    'tabu_ratio FLOAT NOT NULL,' \
                                    'built_year INTEGER NOT NULL,' \
                                    'size FLOAT NOT NULL, ' \
                                    'updated_at datetime NOT NULL, ' \
                                    'rooms_num TEXT NOT NULL, ' \
                                    ' UNIQUE (address, gush_helka));'

        cursor = self.sqlite_connection.cursor()
        self.sqlite_connection.row_factory = sqlite3.Row
        print("Successfully Connected to SQLite")
        cursor.execute(sqlite_create_table_query)

        cursor.execute(f"-- CREATE INDEX IF NOT EXISTS row_info ON {self.table_name} (gush_helka, address);")

        self.sqlite_connection.commit()
        print(f'SQLite "{self.table_name}" table was created')

        cursor.close()

    # todo: supprt list of dealrecords
    def insert(self, deal_records: DealsRecords, address: str):
        func_name = sys._getframe().f_code.co_name
        print(f' {func_name} function with DealsRecords: {deal_records}')
        cursor = self.sqlite_connection.cursor()

        now = datetime.datetime.now()
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")

        insert_query = f"INSERT INTO {self.table_name}" \
                       f" (gush_helka, address, date_of_sale, declared_value, sale_value, deal_type, tabu_ratio, built_year, size, rooms_num, updated_at) " \
                       f"VALUES (?, ?, ?, ?, ?, ?, ?, ?,?,?,?)"

        try:
            cursor.execute(insert_query, (deal_records.gush_helka, address, deal_records.date_of_sale,
                                          deal_records.declared_value, deal_records.sale_value, deal_records.deal_type,
                                          deal_records.ground_ratio, deal_records.built_year, deal_records.size,
                                          deal_records.rooms_num, now_str))
        except sqlite3.IntegrityError as e:
            print(e.__str__())
            if "UNIQUE constraint failed:" in str(e):
                logging.warning(f'The Record already exists in the db. deal_records: {deal_records}')
                return 0
            raise

        if not cursor.lastrowid:
            raise Exception(f'deal_records {deal_records}, failed to be inserted')

        self.sqlite_connection.commit()
        print("Record inserted successfully")
        cursor.close()

    def close(self):
        print("Closing SQL connection")
        self.sqlite_connection.close()
