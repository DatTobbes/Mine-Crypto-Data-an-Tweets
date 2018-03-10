import pymysql


class MySqlDbConnector:

    def __init__(self, Host, Port, User, PassW, DatabaseName ):
        self.host=Host
        self.port=Port
        self.user=User
        self.password=PassW
        self.db=DatabaseName
        #db-Connection wird in jeder Methode gehandelt
        #self.conn = pymysql.connect(host=Host, port=Port, user=User, passwd=PassW, db=DatabaseName)

    def __createConnection(self):
        try:
            return pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.password, db=self.db)
        except:
            print("Connection failt")

    #Versucht eine Abfrage auf die Tabelle,
    #falls diese nicht vorhanden ist wird eine Exception gemeldet
    def __checkIfExists(self,tableName):
        try:
            connection= self.__createConnection()
            cur = connection.cursor()
            stmt = "SHOW TABLES LIKE "+tableName
            cur.execute(stmt)
            result = cur.fetchone()
            connection.close()
            if result:
                return True
            else:
                return False

        except:
            print("Diese Tabelle existiert bereits")

    def __create_table_actual_coindata(self):
        try:
            connection = self.__createConnection()
            cur = connection.cursor()
            sql= """CREATE TABLE `actual_coindata` (
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
            cur.execute(sql)
            print("Tablle actual_coindata wurde erstellt")
            connection.close()
        except:
            print("Fehler beim erstellen der Tabelle actual_coindata")

    #diese Methode erstellt eine Tablle für jeden angegeben Coin.
    def create_table_for_important_coins(self,coinName):
        print("Erstelle Datenbanktabelle für coin %s" %coinName)
        try:
            connection = self.__createConnection()
            cur = connection.cursor()
            sql= """CREATE TABLE  `%s` (
                  `short_name` varchar(10) DEFAULT NULL,
                  `unixTimeStamp` int(11) NOT NULL,
                  `mktcap` float NOT NULL,
                  `price` float NOT NULL,
                  `volume` float NOT NULL,
                  `primaryKey` int(11) NOT NULL AUTO_INCREMENT,
                   PRIMARY KEY (`primaryKey`)
                    )"""
            cur.execute(sql, coinName)
            print("Tablle %s wurde erstellt" %coinName)
            connection.close()
        except Exception as inst:
            print("Fehler beim erstellen der Tabelle %s" %coinName)
            print(inst)

    def select(self, sql):
        connection= self.__createConnection()
        cur = connection.cursor()
        cur.execute(sql)
        print(cur.description)
        # for row in cur:
        #     print(row)
        query_data= cur.fetchall()
        cur.close()
        connection.close()
        return  query_data

    #Schreibt das Ergebnis von  http://coincap.io/front in die Tabelle actual_coindata
    def insertFrontData(self,valuesToInsert):
        try:
             connection = self.__createConnection()
             with connection.cursor() as cursor:
                sql = "INSERT INTO actual_coindata (cap24hrChange,long_name, mktcap ,perc,price,shapeshift,short_name,supply,usdVolume,volume,vwapData,vwapDataBTC) VALUES " \
                      + "," .join("(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" for val in valuesToInsert)
                sortedCionData=self.sortValues(valuesToInsert)
                flattened_values = [item for sublist in sortedCionData for item in sublist]
                cursor.execute(sql,flattened_values )
                connection.commit()

             connection.close()
        except:
            print("Fehler bei insertFrontData")

    def sortValues(self, values):
        newList=[]
        for coin in values:
            newList.append([value for (key, value) in sorted(coin.items())])
        return newList

    #Später könnten mehr Tabellen folgen
    def createTables(self):
        self.__create_table_actual_coindata()


if __name__ == "__main__":
    def parser(x):
        from pandas import datetime
        #return datetime.strptime('190' + x, '%Y-%m')
        return datetime.strptime( x, '%Y-%m-%d %H:%M:%S')

    con= MySqlDbConnector('localhost', 3306, 'root', '', 'coindata')
    test =con.select("SELECT time, price FROM actual_coindata WHERE short_name='BTC' ")

    import csv

    with open('BTC.csv', 'w', newline='') as csvfile:
        fieldnames = ['time', 'price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for line in test:
            writer.writerow({'time': line[0], 'price': line[1]})


