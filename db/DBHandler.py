from pymongo import MongoClient


# DBs
ASCLEPIO = "asclepio"

# Collections
DOCTORS = "doctors"


class DBHandler:
    def __enter__(self):
        return self

    def __init__(self):
        self.mongo_client = MongoClient(host="localhost", port=27017)

        self.asclepio = self.mongo_client[ASCLEPIO]

    def get_doctors(self):
        return self.asclepio[DOCTORS]

    def close(self):
        if self.mongo_client is not None:
            self.mongo_client.close()

    def __exit__(self, _type, value, traceback):
        self.close()
