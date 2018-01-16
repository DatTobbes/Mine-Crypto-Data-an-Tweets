from Service.AskCoincap import CoinIoReader
from Database.db_mongo import MongoDBConnector

coinReader = CoinIoReader()

db_mongo = MongoDBConnector('localhost', 27017)
db_mongo.insert_coin_data(coinReader.getCoinCapFrontData())
db_mongo.close_connector()
