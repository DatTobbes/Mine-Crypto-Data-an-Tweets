import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import time
import json
from SentimentAnalyze import SentimentAnalyzer
from Database.db_mySql import MySqlDbConnector

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
        self.db_connector= MySqlDbConnector('localhost', 3306, 'root', '', 'coindata')
        self.db_connector.create_tweets_tabel()

    def __format_tweet(self,tweet_as_json):
        tweet_as_list=[]
        all_data = json.loads(tweet_as_json)
        tweet_as_list.append(all_data['text'])

        if all_data['retweeted']:
            tweet_as_list.append(1)
        elif not all_data['retweeted']:
            tweet_as_list.append(0)


        tweet_as_list.append(all_data['retweet_count'])

        sentiment= self.analyzer.analyze_tweet(all_data['text'])
        tweet_as_list.append(sentiment['pos'])
        tweet_as_list.append(sentiment['neg'])
        tweet_as_list.append(sentiment['neu'])
        tweet_as_list.append(sentiment['compound'])
        tweet_as_list.append(0)

        return tweet_as_list

    def on_data(self, data):
        try:
            tweet= self.__format_tweet(data)
            print(tweet)

            self.db_connector.insertTweets(tweet)
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True

twitter_stream = Stream(auth, CryptoListner())
twitter_stream.filter(languages=['en'],track=['#BTC', '#bitcoin', '#eth','#iota' '#ETH', '#dash', '#DASH', '#crypto', '#cryptocurrency', '#bitcoin cash', '#bch', '#XRP', '#BCH'])