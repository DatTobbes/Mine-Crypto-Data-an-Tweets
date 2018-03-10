import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import time
import json
from SentimentAnalyze import SentimentAnalyzer

json_keys= open("keys.json").read()
keys= json.loads(json_keys)

consumer_key = keys["consumer_key"]
consumer_secret = keys["consumer_secret"]
access_token = keys["access_token"]
access_secret = keys["access_secret"]


auth = OAuthHandler(keys["consumer_key"], keys["consumer_secret"])
auth.set_access_token(keys["access_token"], keys["access_secret"])

api = tweepy.API(auth)

class CryptoListner(StreamListener):
    def __init__(self):
        self.analyzer = SentimentAnalyzer()

    def on_data(self, data):
        try:

            all_data= json.loads(data)
            timestamp= all_data['timestamp_ms']
            tweet= all_data['text']
            geo=all_data['geo']
            retweet_count= all_data['retweet_count']
            sentiment= self.analyzer.analyze_tweet(tweet)
            print(timestamp,tweet, sentiment )
            # with open('python.json', 'a') as f:
            #     #print(json.loads(data))
            #     f.write(data)
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True

twitter_stream = Stream(auth, CryptoListner())
twitter_stream.filter(languages=['en'],track=['#BTC', '#bitcoin', '#eth','#iota' '#ETH', '#dash', '#DASH', '#crypto', '#cryptocurrency', '#bitcoin cash', '#bch', '#XRP', '#BCH'])