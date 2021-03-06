"""
Create a Mysql Database for storing historical cryptocurrency data
"""

import pymysql


class MySqlDbConnector:
    def __init__(self, Host, Port, User, PassW, DatabaseName):
        self.host = Host
        self.port = Port
        self.user = User
        self.password = PassW
        self.db = DatabaseName

    def __createConnection(self):
        try:
            return pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.password, db=self.db,
                                   use_unicode=True, charset="utf8")
        except:
            print("Connection failt")

    def __checkIfExists(self, table_name):
        try:
            connection = self.__createConnection()
            cur = connection.cursor()
            stmt = "SHOW TABLES LIKE " + table_name
            cur.execute(stmt)
            result = cur.fetchone()
            connection.close()
            if result:
                return True
            else:
                return False

        except:
            print("Diese Tabelle existiert bereits")

    def __create_table_actual_coindata(self, coin_name):
        try:
            connection = self.__createConnection()
            cur = connection.cursor()
            sql = """CREATE TABLE `%s` (
                  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  `short_name` varchar(10) DEFAULT NULL,
                  `long_name` varchar(20) DEFAULT NULL,
                  `mktcap` float DEFAULT NULL,
                  `price` float DEFAULT NULL,
                  `cap24hrChange` float DEFAULT NULL,
                  `perc` float DEFAULT NULL,
                  `shapeshift` varchar(5) DEFAULT NULL,
                  `supply` float DEFAULT NULL,
                  `usdVolume` float DEFAULT NULL,
                  `volume` float DEFAULT NULL,
                  `vwapData` float DEFAULT NULL,
                  `vwapDataBTC` float DEFAULT NULL,
                  `primaryKey` int(11) NOT NULL AUTO_INCREMENT,
                   PRIMARY KEY (`primaryKey`)
                    )"""
            cur.execute(sql, coin_name)
            print("Tablle %s wurde erstellt" % coin_name)
            connection.close()
        except Exception as e:
            print(e.message)
            print("Fehler beim erstellen der Tabelle %s" % coin_name)


    def create_table_for_important_coins(self, coinName):
        print("Erstelle Datenbanktabelle für coin %s" % coinName)
        try:
            connection = self.__createConnection()
            cur = connection.cursor()
            sql = """CREATE TABLE  `%s` (
                  `short_name` varchar(10) DEFAULT NULL,
                  `unixTimeStamp` int(11) NOT NULL,
                  `mktcap` float NOT NULL,
                  `price` float NOT NULL,
                  `volume` float NOT NULL,
                  `primaryKey` int(11) NOT NULL AUTO_INCREMENT,
                   PRIMARY KEY (`primaryKey`)
                    )"""
            cur.execute(sql, coinName)
            print("Tablle %s wurde erstellt" % coinName)
            connection.close()
        except Exception as inst:
            print("Fehler beim erstellen der Tabelle %s" % coinName)
            print(inst)

    def select(self, sql):
        connection = self.__createConnection()
        cur = connection.cursor()
        cur.execute(sql)
        print(cur.description)

        query_data = cur.fetchall()
        cur.close()
        connection.close()
        return query_data

    def insertFrontData(self, valuesToInsert):
        try:
            connection = self.__createConnection()
            with connection.cursor() as cursor:
                sql = "INSERT INTO actual_coindata (cap24hrChange,long_name, mktcap ,perc,price,shapeshift,short_name,supply,usdVolume,volume,vwapData,vwapDataBTC) VALUES " \
                      + ",".join("(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" for val in valuesToInsert)
                sortedCionData = self.sortValues(valuesToInsert)
                flattened_values = [item for sublist in sortedCionData for item in sublist]
                cursor.execute(sql, flattened_values)
                connection.commit()

            connection.close()
        except:
            print("Fehler bei insertFrontData")

    def sortValues(self, values):
        newList = []
        for coin in values:
            newList.append([value for (key, value) in sorted(coin.items())])
        return newList


    def create_actual_coindata_table(self):
        self.__create_table_actual_coindata('actual_coindata')

    def create_tweets_tabel(self):
        if not self.__checkIfExists('tweets'):
            self.__create_table_tweet()

    def __create_table_tweet(self):
        try:
            connection = self.__createConnection()
            cur = connection.cursor()
            sql = """CREATE TABLE `tweets` (
                  `time_stamp` int(15) NOT NULL,
                  `tweet_text` varchar(280) DEFAULT NULL,
                  `retweeted` tinyint(1) DEFAULT NULL,
                  `retweet_count` int(6) DEFAULT NULL,
                  `sentiment_pos` float DEFAULT NULL,
                  `sentiment_neg` float DEFAULT NULL,
                  `sentiment_neu` float DEFAULT NULL,
                  `sentiment_comp` float DEFAULT NULL,
                  `price_diff` tinyint(1) DEFAULT NULL,
                  `start_price` float DEFAULT NULL,
                  `end_price` float DEFAULT NULL,
                  `primaryKey` int(11) NOT NULL AUTO_INCREMENT,
                   PRIMARY KEY (`primaryKey`)
                    )"""
            cur.execute(sql)
            print("Tablle tweet  wurde erstellt")
            connection.close()
        except:
            print("Fehler beim erstellen der Tabelle tweet")

    def insertTweets(self, valuesToInsert):

        connection = self.__createConnection()
        with connection.cursor() as cursor:
            sql = "INSERT INTO tweets (time_stamp," \
                  "tweet_text," \
                  "retweeted," \
                  " retweetet_count," \
                  "sent_pos," \
                  "sent_neg," \
                  "sent_neu, " \
                  "sent_comb," \
                  "price_diff, " \
                  "start_price, " \
                  "end_price ) " \
                  "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, valuesToInsert)
            connection.commit()

        connection.close()

    def create_table_with_name(self, table_name):
        self.__create_table_actual_coindata(table_name)

