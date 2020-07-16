class ForSalePropertyRecord(object):

    def __init__(self, row):
        self.id = row['id']
        self.address = row['address']
        self.rooms = float(row['rooms'])
        self.floor_num = float(row['floor_num'])
        self.size = float(row['size'])
        self.price = float(row['price'])
        self.created_at = row['created_at']
        self.updated_at = row['updated_at']
        self.gush = row['gush']
        self.helka = row['helka']
        self.compare_average = row['compare_average']  # to update

    def __repr__(self):
        return str(self.__dict__)
