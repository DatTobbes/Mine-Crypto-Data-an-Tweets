from pymongo import MongoClient
import re
import time
import logging
logger = logging.getLogger(__name__)


class MongoDBConnector:
    def __init__(self, host, port):
        self.client = MongoClient(host,port)
        self.db = self.client.stockprediction

    def insert_coin_data(self, values):
        start = time.time()
        # sort values by market cap descending
        sorted_values = sorted(values, key=lambda value: value['mktcap'], reverse=True)

        for i in range(0, 20):
            # remove nasty characters in short names
            coin_name = re.sub('[./]', '', sorted_values[i]['long'])
            if coin_name:
                collection = self.db[coin_name]
                collection.insert_one(sorted_values[i])
        logger.info('Time creating DB entries: ' + str(time.time() - start))

    def close_connector(self):
        self.client.close()
