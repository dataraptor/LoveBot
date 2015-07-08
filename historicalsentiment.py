import tweepy
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob
from elasticsearch import Elasticsearch

# import twitter keys and tokens
from config import *

# create instance of elasticsearch
es = Elasticsearch()

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
query = raw_input("Twitter search term: ")
for data in tweepy.Cursor(api.search, q=query).items():
    print data.text
    tweet = TextBlob(data.text)

    print tweet.sentiment.polarity

    # determine if sentiment is positive, negative, or neutral
    if tweet.sentiment.polarity < 0:
        sentiment = "negative"
    elif tweet.sentiment.polarity > 0.05:
        sentiment = "positive"
    else:
        sentiment = "neutral"

    # output sentiment
    print sentiment

    # add text and sentiment info to elasticsearch
    es.index(index="sentiment",
             doc_type="test-type",
             body={"author": data.user.screen_name,
                   "date": data.created_at,
                   "message": data.text,
                   "polarity": tweet.sentiment.polarity,
                   "subjectivity": tweet.sentiment.subjectivity,
                   "sentiment": sentiment})