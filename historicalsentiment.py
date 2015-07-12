import tweepy
import numpy
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob
from elasticsearch import Elasticsearch

# import twitter keys and tokens
from config import *

es = Elasticsearch()
#Set the query variable

def twitter_scraper(query, i):
    for data in tweepy.Cursor(api.search, q=query).items():
        print data.text
        text = TextBlob(data.text)

        polarity = text.sentiment.polarity
        print polarity

        # determine if sentiment is positive, negative, or neutral
        if polarity < 0:
            sentiment = "negative"
        elif polarity > 0.05:
            sentiment = "positive"
        else:
            sentiment = "neutral"

        # output sentiment
        print sentiment

        es.index(index=str(i),
                     doc_type="test-type",
                     body={"author": data.user.screen_name,
                           "date": data.created_at,
                           "message": data.text,
                           "polarity": polarity,
                           "subjectivity": text.sentiment.subjectivity,
                           "sentiment": sentiment})

if __name__ == '__main__':
    #Authenticate via Twitter
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    index = raw_input("Elasticsearch index: ")
    term = raw_input("Twitter search term: ")
    twitter_scraper(term, index)