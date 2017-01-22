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
client = MongoClient('mongodb://admin:admin@catscratchdb-shard-00-00-pvqvd.mongodb.net:27017,catscratchdb-shard-00-01-pvqvd.mongodb.net:27017,catscratchdb-shard-00-02-pvqvd.mongodb.net:27017/admin?ssl=true&replicaSet=CatScratchDB-shard-0&authSource=admin')
#client = MongoClient('mongodb://localhost:27017/')

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
        self.dict = {"stupid": "SPACE CAT",
                     "Stupid": "SPACE CAT",
                     "STUPID":"SPACE CAT",
                     "stupid.":"SPACE CAT",
                     "fuck": "SPACE CAT",
                     "fuck.":"SPACE CAT",
                     "Fuck":"SPACE CAT",
                     "FUCK":"SPACE CAT",
                     "shit": "SPACE CAT",
                     "Shit": "SPACE CAT",
                     "SHIT": "SPACE CAT",
                     "shit.": "SPACE CAT",
                     "cunt": "SPACE CAT",
                     "cunt.": "SPACE CAT",
                     "CUNT": "SPACE CAT",
                     "Cunt": "SPACE CAT",
                     "piss": "SPACE CAT",
                     "piss.": "SPACE CAT",
                     "Piss": "SPACE CAT",
                     "PISS": "SPACE CAT",
                     "ass": "SPACE CAT",
                     "ass.": "SPACE CAT",
                     "Ass": "SPACE CAT",
                     "ASS": "SPACE CAT",
                     "butt": "SPACE CAT",
                     "butt.": "SPACE CAT",
                     "Butt":"SPACE CAT",
                     "BUTT":"SPACE CAT",
                     "loser": "SPACE CAT",
                     "nigger": "SPACE CAT",
                     "crap": "SPACE CAT",
                     "damn": "SPACE CAT",
                     "bitch": "SPACE CAT",
                     "dammit": "SPACE CAT",
                     "douche": "SPACE CAT",
                     "ugly": "SPACE CAT",
                     "suck": "SPACE CAT",
                     "dork": "SPACE CAT",
                     "wtf": "SPACE CAT",
                     "dick": "SPACE CAT",
                     "retard": "SPACE CAT",
                     "fag": "SPACE CAT",
                     "whore": "SPACE CAT",
                     "butt": "SPACE CAT",
                     "dumb": "SPACE CAT",
                     "idiot": "SPACE CAT",
                     "Michigan": "SPACE CAT"
                     }
        self.tweetCount = 0
        #self.tweet_dict = {}

    def multiple_replace(self,text):
        # Create a regular expression  from the dictionary keys
        regex = re.compile("(%s)" % "|".join(map(re.escape, self.dict.keys())))

        # For each match, look-up corresponding value in dictionary
        return regex.sub(lambda mo: self.dict[mo.string[mo.start():mo.end()]], text)


    def on_data(self,data):
        json_tweet = json.loads(data)
        tweet = json_tweet["text"]
        tweet_dict = {}
        #tweet = data.split(',"text":"')[1].split('","source')[0]
        new_tweet = self.multiple_replace(tweet)

        users_dict = json_tweet["entities"]
        user_mentions = users_dict["user_mentions"]
        screen_name = "Private"
        if (len(user_mentions)>0):
            um_sub = user_mentions[0]
            screen_name = um_sub["screen_name"]

        user_id = json_tweet["user"]
        profile_picture_url = user_id["profile_image_url"]

        #self.tweets.append(data)
        self.tweetCount = self.tweetCount + 1
        tweet_dict['screen_name'] = screen_name
        tweet_dict['profile_picture'] = profile_picture_url
        tweet_dict['old_tweet'] = tweet
        tweet_dict['tweet_text'] = new_tweet
        # saveFile = open('newTwitDB.json','a')
        # saveFile.write(new_tweet)
        # saveFile.write('\n')
        # saveFile.close()
        tweets.insert_one(tweet_dict)
        return self.tweetCount < 20


    def on_error(self,status):
        print(status)

keyword = sys.argv[1]
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track = [keyword])
