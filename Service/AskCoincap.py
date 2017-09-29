import requests
import json


class CoinIoReader:
    def __init__(self):
        self.url = "http://coincap.io/"


    def getCoinCapData(self,argument):
        response = requests.get(self.url+argument)
        if (response.ok):
            print("\n")
            content = response.content
            json_data = json.loads(response.text)
            return json_data
        else:
            response.raise_for_status()

    #Methode wird noch nicht verwendet
    def getMostImportantCoins(self):
        allCoins= self.getCoinCapData('front')
        importantCoinList=[]
        for coins in allCoins:
            if coins["mktcap"] >=1000000000:
                importantCoinList.append(coins["short"])
        return importantCoinList

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
