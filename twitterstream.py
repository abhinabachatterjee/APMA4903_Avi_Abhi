from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import pymysql
import time
import json
#import sentiment_mod as s

#        replace mysql.server with "localhost" if you are running via your own server!
#                        server       MySQL username	MySQL pass  Database name.
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='twitterstream',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


c = conn.cursor()

# consumer key, consumer secret, access token, access secret.
ckey = "g2Szmw9CdlqJoLnuxHymkBBNY"
csecret = "poDGfMIfnqXKLi75FGpuy6NmfjHK0P9Xr9wOPNFpcCiPWCD53B"
atoken = "735946611264761856-LQPOjTm8OukyU9KvE3xqLdxcfKxIcxO"
asecret = "D9DYE90J97hDBrtNVDsu6lXzlMENv0BjjGyRVmkvaPcw6"


class listener(StreamListener):
    def on_data(self, data):
        all_data = json.loads(data)

        tweet = all_data["text"]
        username = all_data["user"]["screen_name"]

        if all_data["coordinates"]:
            coord = all_data["coordinates"]
            c.execute("INSERT INTO geotag (times, username, coord) VALUES (%s,%s,%s)", (time.time(), username, coord))

        c.execute("INSERT INTO twitterdata (times, username, tweet) VALUES (%s,%s,%s)", (time.time(), username, tweet))


        conn.commit()

        #sent_value, confidence = s.sentiment(tweet)
        #print(tweet)
        #if confidence*100 >= 80:
         #   output = open("twitter-out.txt", "a")
          #  output.write(sent_value)
          #  output.write('\n')
          #  output.close()
        #return True

    def on_error(self, status):
        print(status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["car"])