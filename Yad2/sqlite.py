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

        sqlite_create_table_query = 'CREATE TABLE if NOT EXISTS yad2_records (' \
                                    'id INTEGER PRIMARY KEY,' \
                                    'address TEXT  NOT NULL,' \
                                    'rooms TEXT NOT NULL, ' \
                                    'floor_num TEXT NOT NULL, ' \
                                    'size TEXT NOT NULL, ' \
                                    'price TEXT NOT NULL, ' \
                                    'created_at datetime NOT NULL, ' \
                                    'updated_at datetime NOT NULL, ' \
                                    ' UNIQUE (address, rooms, floor_num, size, price));'

        cursor = self.sqlite_connection.cursor()
        self.sqlite_connection.row_factory = sqlite3.Row
        print("Successfully Connected to SQLite")
        cursor.execute(sqlite_create_table_query)

        cursor.execute("CREATE INDEX IF NOT EXISTS row_info ON yad2_records (address, rooms, floor_num, size, price);")

        self.sqlite_connection.commit()
        print("SQLite table created")

        cursor.close()

    def insert(self, row_info):
        print('row_info={}'.format(row_info))
        cursor = self.sqlite_connection.cursor()

        now = datetime.datetime.now()
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")

        insert_query = "INSERT INTO yad2_records (address, rooms, floor_num, size, price, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)".format(
            self.table_name)

        try:
            cursor.execute(insert_query, (row_info.address, row_info.rooms, row_info.floor_num,
                                          row_info.size, row_info.price,
                                          now_str, now_str))
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

    # def update_file_path_fixed(self,row_info):
    #     query = "UPDATE {} SET 'was_fixed' = '{}', updated_at = '{}' WHERE service_id = '{}' AND corrupted_path = '{}' " \
    #         .format(self.TABLE_NAME, datetime.datetime.now(), datetime.datetime.now(), service_id, corrupted_path)
    # self.sqlite_connection.cursor().execute(query)
    # self.sqlite_connection.commit()

    def close(self):
        print("Closing SQL connection")
        self.sqlite_connection.close()
