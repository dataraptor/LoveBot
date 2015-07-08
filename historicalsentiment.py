#!/usr/bin/env python

import tweepy
import numpy as np
import pandas as pd
import json
import csv
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob

# import twitter keys and tokens
from config import *

#Authenticate via Twitter
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#Set the query variable
query = "Congress"
#query = raw_input("Twitter search term: ")

#Initialize tweets matrix
tweet_matrix = []

#Retrieve historical tweets, parse for selected information and append vectors to matrix
historical_tweets = tweepy.Cursor(api.search, q=query).items(10)
for tweet in historical_tweets:
    try:
        if tweet.retweeted_status:
            tweet_vector = [tweet.retweeted, tweet.author.screen_name, tweet.retweeted_status.text, tweet.coordinates]
            print tweet.retweeted_status.text
    except:
        tweet_vector = [tweet.retweeted, tweet.author.screen_name, tweet.text, tweet.coordinates]
        print tweet.text
    tweet_matrix.append(tweet_vector)

with open("tweets.csv", "wb") as f:
    writer = csv.writer(f)
    for row in tweet_matrix:
        try:
            writer.writerow(row)
        except Exception, e:
            pass

def polarity(s):
    blob = TextBlob(s)
    print blob
'''
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
'''