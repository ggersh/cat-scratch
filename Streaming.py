import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import pymongo
#from Tokenizer import *
import time
import re
import json

from pymongo import MongoClient
#client = MongoClient('mongodb://admin:admin@catscratchdb-shard-00-00-pvqvd.mongodb.net:27017,catscratchdb-shard-00-01-pvqvd.mongodb.net:27017,catscratchdb-shard-00-02-pvqvd.mongodb.net:27017/admin?ssl=true&replicaSet=CatScratchDB-shard-0&authSource=admin')
client = MongoClient('mongodb://localhost:27017/')

db = client['catscratch']
tweets = db['tweets']
db.tweets.delete_many({})
ckey = 'lDxRlm3XWcEBIO7D8q8idMebz'
csecret = 'Cy6M1nKIq2aJyyuQRuscB0B8qDPPYpmxTHdwgOJts6L62YaK8e'
atoken = '4748567247-oYYHCKqGcsIG9KItdNKtLNzqAEOXXcsNVeLFswI'
asecret = 'yFV5J8TV61kRFiip5teaUFvkwdDlMClWs7kXCqiTmFeOi'

class listener(StreamListener):
    def __init__(self):

        self.tweets = []
        self.dict = {"stupid":'&#x1f431',
                     "Stupid":'&#x1f431',
                     "STUPID":'&#x1f431',
                     "stupid.":'&#x1f431',
                     "fuck": '&#x1f680',
                     "fuck.":'&#x1f319',
                     "Fuck":'&#x1f319',
                     "FUCK":'&#x1f319',
                     "shit": '&#x1f319',
                     "Shit": '&#x1f319',
                     "SHIT": '&#x1f319',
                     "shit.": '&#x1f319',
                     "cunt": '&#x1f431',
                     "cunt.": '&#x1f431',
                     "CUNT": '&#x1f431',
                     "Cunt": '&#x1f431',
                     "piss": '&#x1f680',
                     "piss.": '&#x1f680',
                     "Piss": '&#x1f680',
                     "PISS": '&#x1f680',
                     "ass": '&#x1f319',
                     "ass.": '&#x1f319',
                     "Ass": '&#x1f319',
                     "ASS": '&#x1f319',
                     "butt":'&#x1f431',
                     "butt.":'&#x1f431',
                     "Butt":'&#x1f431',
                     "BUTT":'&#x1f431',
                     "loser": '&#x1f680',
                     "nigger": '&#x1f431',
                     "crap": '&#x1f431',
                     "damn": '&#x1f431',
                     "bitch": '&#x1f680',
                     "dammit": '&#x1f431',
                     "douche": '&#x1f431',
                     "ugly": '&#x1f680',
                     "suck": '&#x1f431',
                     "dork": '&#x1f431',
                     "wtf": '&#x1f680',
                     "dick": '&#x1f431',
                     "retard": '&#x1f431',
                     "fag": '&#x1f680',
                     "whore": '&#x1f431',
                     "butt": '&#x1f431',
                     "dumb": '&#x1f680',
                     }
        self.tweetCount = 0
        #self.tweet_dict = {}

    def multiple_replace(self,text):
        # Create a regular expression  from the dictionary keys
        regex = re.compile("(%s)" % "|".join(map(re.escape, self.dict.keys())))

        # For each match, look-up corresponding value in dictionary
        return regex.sub(lambda mo: self.dict[mo.string[mo.start():mo.end()]], text)


    def on_data(self,data):
        #print"*******DATA*********\n"
        #print data+"\n"
        json_tweet = json.loads(data)
        tweet = json_tweet["text"]
        tweet_dict = {}
        #tweet = data.split(',"text":"')[1].split('","source')[0]

        new_tweet = self.multiple_replace(tweet)

        users_dict = json_tweet["entities"]
        user_mentions = users_dict["user_mentions"]
        screen_name = ""
        if (len(user_mentions)>0):
            um_sub = user_mentions[0]
            screen_name = um_sub["screen_name"]

        user_id = json_tweet["user"]
        profile_picture_url = user_id["profile_image_url"]

        #self.tweets.append(data)
        # print(new_tweet)
        self.tweetCount = self.tweetCount + 1
        tweet_dict['screen name' + str(self.tweetCount)] = screen_name
        tweet_dict['profile picture' + str(self.tweetCount)] = profile_picture_url
        tweet_dict['old_tweet' + str(self.tweetCount)] = tweet
        tweet_dict['tweet_text' + str(self.tweetCount)] = new_tweet
        # print "********tweet_dict*********\n"
        # print tweet_dict
        # saveFile = open('newTwitDB.json','a')
        # saveFile.write(new_tweet)
        # saveFile.write('\n')
        # saveFile.close()

        tweets.insert_one(tweet_dict)

        return self.tweetCount < 30


    def on_error(self,status):
        print(status)

keyword = sys.argv[1]
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track = [keyword])
