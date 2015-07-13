import tweepy
import json
import csv
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
tweets = []

def scrape(query):
    print "Searching for matching tweets and analyzing sentiment..."
    for data in tweepy.Cursor(api.search, q=query).items():
        
        text = TextBlob(data.text)
        polarity = text.sentiment.polarity

        # determine if sentiment is positive, negative, or neutral
        if polarity < 0:
            sentiment = "negative"
        else:
            sentiment = "positive"

        tweets.append({
            "author": data.user.screen_name,
            "date": data.created_at,
            "message": data.text,
            "polarity": polarity,
            "subjectivity": text.sentiment.subjectivity,
            "sentiment": sentiment
            })
    print "...done."
    return tweets

'''def export_csv():
    print "Exporting to csv..."
    f = open('tweets.csv', 'w', newline = '')
    for tweet in tweets:
        tweet.date = tweet.date.date()
'''

if __name__ == "__main__":
    query = "@Betterment"
    scrape(query)