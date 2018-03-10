import tweepy
import json
from tweepy import OAuthHandler
import time
json_keys= open("keys.json").read()
keys= json.loads(json_keys)

auth = OAuthHandler(keys["consumer_key"], keys["consumer_secret"])
auth.set_access_token(keys["access_token"], keys["access_secret"])

api = tweepy.API(auth)


searchQuery = 'BTC'

while True:
    new_tweets = api.search(q=searchQuery, since_id=id, )

    print(new_tweets.max_id, new_tweets.since_id)
    print(len(new_tweets))
    id= new_tweets.max_id
    time.sleep(0.5)

