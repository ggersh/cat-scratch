import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
#from Tokenizer import *
import time
import re
import json

from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')

db = client['catscratch']
tweets = db['tweets']

ckey = 'lDxRlm3XWcEBIO7D8q8idMebz'
csecret = 'Cy6M1nKIq2aJyyuQRuscB0B8qDPPYpmxTHdwgOJts6L62YaK8e'
atoken = '4748567247-oYYHCKqGcsIG9KItdNKtLNzqAEOXXcsNVeLFswI'
asecret = 'yFV5J8TV61kRFiip5teaUFvkwdDlMClWs7kXCqiTmFeOi'

class listener(StreamListener):
    def __init__(self):
        self.tweets = []
        self.dict = {"cavs":'Super Team'}
        self.tweetCount = 0
        self.tweet_dict = {}

    def multiple_replace(self,text):
        # Create a regular expression  from the dictionary keys
        regex = re.compile("(%s)" % "|".join(map(re.escape, self.dict.keys())))

        # For each match, look-up corresponding value in dictionary
        return regex.sub(lambda mo: self.dict[mo.string[mo.start():mo.end()]], text)


    def on_data(self,data):
        json_tweet = json.loads(data)
        tweet = json_tweet["text"]
        #tweet = data.split(',"text":"')[1].split('","source')[0]

        new_tweet = self.multiple_replace(tweet)

        #self.tweets.append(data)
        # print(new_tweet)
        self.tweetCount = self.tweetCount + 1
        self.tweet_dict['tweet_text' + str(self.tweetCount)] = new_tweet
        # print self.tweetCount
        #
        # saveFile = open('newTwitDB.json','a')
        # saveFile.write(new_tweet)
        # saveFile.write('\n')
        # saveFile.close()

        tweets.insert_one(tweet_dict)

        return self.tweetCount < 7


    def on_error(self,status):
        print(status)

keyword = sys.argv[1]
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track = [keyword])
