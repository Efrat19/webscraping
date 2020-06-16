import datetime
import logging
import os
import sqlite3

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)


class CityRecordsSqlite(object):
    FIELDS = ['id', 'address', 'service_id', 'updated_at', 'created_at', 'was_fixed']
    table_name = 'yad2_records'

    def __init__(self, city_name, path=None):
        print("Starting initialization of the SQLite")
        self.db_name = '{}.db'.format(city_name)
        db_path = os.path.join(path, 'sqlite_' + self.db_name)
        self.sqlite_connection = sqlite3.connect(db_path)

        sqlite_create_table_query = 'CREATE TABLE if NOT EXISTS "{}" (' \
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
                                    ' UNIQUE (address, rooms, floor_num, size, price));' \
            .format(self.table_name)

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

    def update_file_path_fixed(self, row_info, gush, helka):
        query = "UPDATE {} SET updated_at = '{}', gush = '{}', helka = '{}' " \
                "WHERE address = '{}' AND rooms = '{}' AND floor_num = '{}' AND size = '{}' AND price = '{}'" \
            .format(self.table_name, datetime.datetime.now(), gush, helka, row_info.address,
                    row_info.rooms, row_info.floor_num, row_info.size, row_info.price)
        self.sqlite_connection.cursor().execute(query)
        self.sqlite_connection.commit()

    def close(self):
        print("Closing SQL connection")
        self.sqlite_connection.close()
