from pymongo import MongoClient
import re
import time
import logging
logging.basicConfig(filename='stockprediction.log', filemode='w', level=logging.INFO, format='%(asctime)s %(message)s')

class MongoDBConnector:
    def __init__(self, host, port):
        self.client = MongoClient(host,port)
        self.db = self.client.stockprediction

    def insert_coin_data(self, values):
        # sort values by market cap descending
        start = time.time()
        sorted_values = sorted(values, key=lambda value: value['mktcap'], reverse=True)

        for i in range(0, 20):
            # remove nasty characters in short names
            coin_name = re.sub('[./]', '', sorted_values[i]['long'])
            if coin_name:
                collection = self.db[coin_name]
                collection.insert_one(sorted_values[i])
        logging.info('Time creating DB entries: ' + str(time.time() - start))

    def close_connector(self):
        self.client.close()
