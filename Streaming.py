import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
#from Tokenizer import *
import time
import re


ckey = 'lDxRlm3XWcEBIO7D8q8idMebz'
csecret = 'Cy6M1nKIq2aJyyuQRuscB0B8qDPPYpmxTHdwgOJts6L62YaK8e'
atoken = '4748567247-oYYHCKqGcsIG9KItdNKtLNzqAEOXXcsNVeLFswI'
asecret = 'yFV5J8TV61kRFiip5teaUFvkwdDlMClWs7kXCqiTmFeOi'

class listener(StreamListener):
    def __init__(self):
        self.tweets = []
        self.dict = {"cavs":u'\ud83d'}

    def multiple_replace(self,text):
        # Create a regular expression  from the dictionary keys
        regex = re.compile("(%s)" % "|".join(map(re.escape, self.dict.keys())))

        # For each match, look-up corresponding value in dictionary
        return regex.sub(lambda mo: self.dict[mo.string[mo.start():mo.end()]], text)


    def on_data(self,data):
        tweet = data.split(',"text":"')[1].split('","source')[0]

        new_tweet = self.multiple_replace(tweet)
        self.tweets.append(data)
        print(new_tweet)


        saveFile = open('newTwitDB.csv','a')
        saveFile.write(new_tweet)
        saveFile.write('\n')
        saveFile.close()
        return True



    def on_error(self,status):
        print(status)


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track = ["cavs"])
