from flask import Flask
from flask import render_template
import json
from pymongo import MongoClient
from bson import json_util
from bson.json_util import dumps

app = Flask(__name__)

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DB_NAME = 'twittersentiment'
COLLECTION_NAME = 'betterment'
FIELDS = {
    "author": True,
    "date": True,
    "message": True,
    "polarity": True,
    "subjectivity": True,
    "sentiment": True,
    '_id': False
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/twittersentiment/betterment")
def twittersentiment_betterment():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DB_NAME][COLLECTION_NAME]
    tweets = collection.find()
    json_tweets = []
    for tweet in tweets:
        json_tweets.append(tweet)
    json_tweets = json.dumps(json_tweets, default = json_util.default)
    connection.close()
    return json_tweets

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000, debug = True)