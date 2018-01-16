import requests
import json
import time
import logging
logger = logging.getLogger(__name__)


class CoinIoReader:
    def __init__(self):
        self.url = "http://coincap.io/"


    # Get : http://coincap.io/front/
    def getCoinCapFrontData(self):
        start = time.time()
        content= self.getCoinCapData('front')
        json_data = json.loads(content.text)
        logger.info("Time GET: " + str(time.time() - start))
        return json_data

    #Get Befehl
    def getCoinCapData(self,argument):
        response = requests.get(self.url+argument)
        if (response.ok):
            return response
        else:
            response.raise_for_status()


    #Methode wird noch nicht verwendet
    def getMostImportantCoins(self, minMktCap):
        allCoins= self.getCoinCapFrontData()
        importantCoinList=[]
        for coins in allCoins:
            if coins["mktcap"] >=minMktCap:
                importantCoinList.append(coins["short"])
        return importantCoinList


    #Test Methode laeuft noch nicht
    #Content kann nicht in Dict gewandelt werden aber ich schnall nicht wieso
    def getDataOfImportantCoins(self):
        coinDict={}
        importantCoins=self.getMostImportantCoins(10000000000)
        response= self.getCoinCapData('history/365day/BTC')
        for coin in importantCoins:
            response = self.getCoinCapData('history/365day/'+coin)
            dict = response.json()
            coinDict[coin]=dict
        return coinDict

    # Methode wird noch nicht verwendet
    def getCoins(self):
        response = requests.get(self.url + 'coins')
        if (response.ok):
            print("\n")
            test = response.content
            json_data = json.loads(response.text)
            return json_data
        else:
            response.raise_for_status()



if __name__ == "__main__":
    coinreader= CoinIoReader()
    coinreader.getDataOfImportantCoins()