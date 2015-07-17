import tweepy
import json
import csv
from datetime import datetime, date
import time
from bson import json_util
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob
from pymongo import MongoClient

# import twitter keys and tokens
from config import *

#Authenticate via Twitter
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#Pass MongoDB variables
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DB_NAME = 'twittersentiment'
COLLECTION_NAME = 'betterment'
FIELDS = {
    "author": True,
    "message": True,
    "date" : True,
    "polarity": True,
    "subjectivity": True,
    "sentiment": True,
    "_id" : False
}

tweets = []

def test():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DB_NAME][COLLECTION_NAME]
    tweet = collection.find_one(projection=FIELDS)
    #json_tweets = [json.dumps(tweet, default=json_util.default) for tweet in tweets]
    #json_tweets = [json.loads(json_tweet, object_hook=json_util.object_hook) for json_tweet in json_tweets]
    return tweet["date"]

def scrape(query):
    print "Searching for matching tweets and analyzing sentiment..."
    for data in tweepy.Cursor(api.search, q=query).items():
        
        date = data.created_at.strftime("%Y-%m-%d")
        text = TextBlob(data.text)
        polarity = text.sentiment.polarity

        # determine if sentiment is positive, negative, or neutral
        if polarity < 0:
            sentiment = "negative"
        else:
            sentiment = "positive"

        tweets.append({
            "author": data.user.screen_name,
            "date": date,
            "message": data.text,
            "polarity": polarity,
            "subjectivity": text.sentiment.subjectivity,
            "sentiment": sentiment
            })
    print "...done."
    return tweets

def add(data):
    print "Inserting into MongoDB..."
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DB_NAME][COLLECTION_NAME]
    collection.insert(data)
    print "...done."
    connection.close()

def clear():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DB_NAME][COLLECTION_NAME]
    collection.drop()
'''def export_csv():
    print "Exporting to csv..."
    f = open('tweets.csv', 'w', newline = '')
    for tweet in tweets:
        tweet.date = tweet.date.date()
'''

if __name__ == "__main__":
    clear()
    add(scrape("@Betterment"))
#    query = "@Betterment"
#    scrape(query)