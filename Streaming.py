from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
#from Tokenizer import *
import time
from checkForHarassment import multipleReplace

ckey =  'lDxRlm3XWcEBIO7D8q8idMebz'
csecret = 'Cy6M1nKIq2aJyyuQRuscB0B8qDPPYpmxTHdwgOJts6L62YaK8e'
atoken =  '4748567247-oYYHCKqGcsIG9KItdNKtLNzqAEOXXcsNVeLFswI'
asecret = 'yFV5J8TV61kRFiip5teaUFvkwdDlMClWs7kXCqiTmFeOi'

class listener(StreamListener):

    def __init__(self):
        self.tweets = []

    def on_data(self,data):



            tweet = data.split(',"text":"')[1].split('","source')[0]
            #print('\n')
            #print('\n')
            #print('_____________')
            self.tweets.append(data)
            print(tweet)
            newTweet = multipleReplace(tweet)
            print(newTweet)



            #
            # saveFile = open('newTwitDB.csv','a')
            # saveFile.write(tweet)
            # saveFile.write('\n')
            # saveFile.close()
            return True



    def on_error(self,status):
        print(status)


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track = ["ugly"])
