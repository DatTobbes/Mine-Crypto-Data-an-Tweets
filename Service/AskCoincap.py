import requests
import json


class CoinIoReader:
    def __init__(self):
        self.url = "http://coincap.io/"



    # Get : http://coincap.io/front/
    def getCoinCapFrontData(self):
        content= self.getCoinCapData('front')
        json_data = json.loads(content.text)
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


    #Test Methode läuft noch nicht
    #Content kann nicht in Dict gewandelt werden aber ich schnall nicht wieso
    def getDataOfImportantCoins(self):
        importantCoins=self.getMostImportantCoins(1000000000)
        response= self.getCoinCapData('history/365day/BTC')


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