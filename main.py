from Service.AskCoincap import CoinIoReader
from Database.Database import DatabaseConnector
import time


conn= DatabaseConnector('localhost',3306,'root','','coindata')
conn.createTables()
coinReader= CoinIoReader()


#fragt alle 120sec ab -> 15000 durchläufe sind ca 20tage
for x in range(15000):

    start = time.time()
    test = coinReader.getCoinCapFrontData()
    conn.insertFrontData(test)
    querytime= time.time()-start
    timeToSleep= 10-querytime
    print("queryTime: "+str(querytime))
    if timeToSleep < 0:
        timeToSleep=0
    print("timetosleep: "+str(timeToSleep))
    time.sleep(timeToSleep)
