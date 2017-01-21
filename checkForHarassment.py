# from Streaming import *
import re

def multipleReplace(text):


    dict = {
      "ugly" : u'\U0001F431"',
      "weird" : "cool",
      "ass" : "bottom"
    }

    regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))


    return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text)
