'''
Store tweets in database using MongoDB
'''
from __future__ import print_function
import tweepy
import json
from pymongo import MongoClient

MONGO_HOST='mongodb://localhost/twitterdb'
WORDS = ['@realDonaldTrump']

CONSUMER_KEY = "SXOwIe3OvkzoIAvC0HIjCejAh"
CONSUMER_SECRET = "8EGcD2PnBgoLshku0z2wneGwYJVHV3xHE87YuenCCcoLMMlmdu"
ACCESS_TOKEN = "847818218265772032-GlCvGajN8f2x7abc4cKrsezYAWjxiLl"
ACCESS_TOKEN_SECRET = "4YDUTWBEJXPABqCpGkMOWiEUpL5JqKuvffpeWsacDy8Yl"

class StreamListener(tweepy.StreamListener):

    def on_connect(self):
        print("Connected to streaming API")

    def on_error(self, status_code):
        print("An error has occured: " + repr(status_code))
        return False

    def on_data(self, data):
        try:
            client = MongoClient(MONGO_HOST)
            db = client.twitterdb
            data_json = json.loads(data)
            created_at = data_json['created_at']
            text = data_json['text']
            print("Tweet collected at " + str(created_at))
            print(str(text) + "\n")
            db.twitter_search.insert(data_json)
        except Exception as e:
            print(e)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True))
streamer = tweepy.Stream(auth=auth, listener=listener)
print("Tracking: " + str(WORDS))
streamer.filter(track=WORDS)

