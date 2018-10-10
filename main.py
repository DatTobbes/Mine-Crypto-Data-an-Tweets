from service.collect_from_coincap import CoinIoReader
from database.db_mongo import MongoDBConnector
import logging

logging.basicConfig(filename='stockprediction.log', filemode='a', level=logging.INFO, format='%(asctime)s %(message)s')

coinReader = CoinIoReader()

db_mongo = MongoDBConnector('localhost', 27017)
db_mongo.insert_coin_data(coinReader.getCoinCapFrontData())
db_mongo.close_connector()
