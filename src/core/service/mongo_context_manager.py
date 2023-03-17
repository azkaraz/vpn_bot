from pymongo import MongoClient


# Подключается к mongodb и возвращает коллекцию в context manager
class MongoCollection(object):

    def __init__(self, uri, collection, database):
        self.client = MongoClient(uri)
        self.db = self.client.get_default_database(database)
        self.collection = self.db[collection]

    def __enter__(self):
        return self.collection

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.client.close()