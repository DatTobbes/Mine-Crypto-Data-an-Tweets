from pymongo import MongoClient


class MongoDBConnector:
    def __init__(self, host, port):
        self.client = MongoClient(host,port)
        self.db = self.client.stockprediction

    def insert_coin_data(self, values):
        for value in values:
            coin_name = value['long'].replace('.', '')
            if coin_name:
                print(coin_name)
                collection = self.db[coin_name]
                collection.insert_one(value)

    def close_connector(self):
        self.client.close()
