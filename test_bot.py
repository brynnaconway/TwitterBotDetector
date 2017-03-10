#! /usr/bin/python

import sys, tweepy, time

argfile = "bot_tweets.txt" #str(sys.arg[1])

auth = tweepy.OAuthHandler("sL2BOOaip5M1GZxY9wVJenrtz", "sKrE6ONhuxFE2c1YpaI5BdiDp53N6HL8ILVvubIkbqWQqLMXrh") 
auth.set_access_token("840213704021049345-X6wFF3URAXSju75ejwY3StLfgtqDIeO", "1XB36ErfJe71f4VnQbrvYVGeVTetKPUwi72VoiBu6HTBo") 
api = tweepy.API(auth)

filename=open(argfile, 'r')
f=filename.readlines()
filename.close()

for line in f: 
    try: 
        print(line)
        if line != '\n':
            api.update_status(line)
            time.sleep(60) # tweet every 15 minutes
        else: 
            pass
    except Exception as e:
        print(e.reason)
        time.sleep(2) 

#for tweet in tweepy.Cursor(api.search, q='@')

