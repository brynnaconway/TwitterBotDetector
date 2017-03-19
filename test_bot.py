#! /usr/bin/python

import sys, tweepy
from time import sleep

def file_tweets():
    argfile = "bot_tweets.txt" #str(sys.arg[1])
    filename = open(argfile, 'r')
    f = filename.readlines()
    filename.close()

    for line in f: 
        try: 
            print(line)
            if line != '\n':
                api.update_status(line)
                sleep(60) # tweet every minute
            else: 
                pass
        except Exception as e:
            print(e.reason)
            sleep(2)

def retweet(rt, fav): 
    for tweet in tweepy.Cursor(api.search, q='#NDMBB').items(20):
        try: 
            if rt == 1:
                tweet.retweet()
            if fav == 1: 
                tweet.favorite() 
            sleep(10)
        except tweepy.TweepError as e: 
            print(e.reason)
        except StopIteration: 
            break

if __name__ == '__main__': 

    auth = tweepy.OAuthHandler("sL2BOOaip5M1GZxY9wVJenrtz", "sKrE6ONhuxFE2c1YpaI5BdiDp53N6HL8ILVvubIkbqWQqLMXrh") 
    auth.set_access_token("840213704021049345-X6wFF3URAXSju75ejwY3StLfgtqDIeO", "1XB36ErfJe71f4VnQbrvYVGeVTetKPUwi72VoiBu6HTBo") 
    api = tweepy.API(auth)

    file_tweets()
    retweet(1, 0)




