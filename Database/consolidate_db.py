import pandas as pd

from  Database.db_mySql import MySqlDbConnector
from sqlalchemy import create_engine, MetaData
import sqlalchemy as sa

class CoinConsolidator:

    def __init__(self):
        print('Instantiate ')
        self.DB_USER = 'root'
        self.DB_PASSWORD = ''
        self.DB_NAME = 'coindata'
        self.DB_HOST = 'localhost'
        self.DB_CONNECTION_STRING = 'mysql+pymysql://{}:{}@localhost:3306/{}?charset=utf8mb4'.format(self.DB_USER, self.DB_PASSWORD, self.DB_NAME)
        self.db_connection_acutal_coindata= create_engine(self.DB_CONNECTION_STRING, echo=False)

        self.DB_NAME = 'coins'
        self.DB_CONNECTION_STRING = 'mysql+pymysql://{}:{}@localhost:3306/{}?charset=utf8mb4'.format(self.DB_USER, self.DB_PASSWORD, self.DB_NAME)
        self.db_connection= create_engine(self.DB_CONNECTION_STRING, echo=False)


    def get_table_metadata(self, table_name='actual_coindata'):
        META_DATA = MetaData(bind=self.db_connection_acutal_coindata, reflect=True)

        table_metadata = META_DATA.tables[table_name]
        print(table_metadata)

    def get_all_data_from_table(self , table_name):
        '''
        Methode nicht in Gebrauch, läde den gesamten Tabelleninhalt in den Speicher.
        Deshalb bei großer Tabelle sehr unperformant
        :return: 
        '''
        df=pd.read_sql_table(table_name,
                             con=self.db_connection_acutal_coindata)
        return df

    def get_distinct_coins(self, min_volume=500E+6):
        print('Get distinct Coins')
        df = pd.read_sql(con=self.db_connection_acutal_coindata,
                         sql=sa.text("SELECT DISTINCT(long_name) FROM actual_coindata where mktcap >=:param1;"),
                         params={'param1': min_volume})
        return df

    def get_coin_from_database(self, coin="BTC"):
        print("Querying coin %s" %coin)
        df = pd.read_sql(con= self.db_connection_acutal_coindata,
                         sql=sa.text("SELECT * FROM actual_coindata where long_name=:param1;"),
                         params={'param1': coin})
        #df.to_sql('btc', self.db_connection )
        return df

    def create_tables_for_coin(self, coin_name):
        mySqlCon= MySqlDbConnector(Host=self.DB_HOST, User=self.DB_USER, Port=3306, PassW=self.DB_PASSWORD, DatabaseName=self.DB_NAME)
        mySqlCon.create_table_with_name(coin_name)

    def wirte_coin_to_table(self, dataframe, table_name):
        dataframe.to_sql(table_name, self.db_connection)


if __name__ == "__main__":
    c = CoinConsolidator()
    c.get_table_metadata()

    most_relevant_coins= c.get_distinct_coins()

    for index, row in most_relevant_coins.iterrows():
        coin_name = row.long_name
        df = c.get_coin_from_database(coin=coin_name)
        c.wirte_coin_to_table(dataframe=df, table_name=coin_name)
