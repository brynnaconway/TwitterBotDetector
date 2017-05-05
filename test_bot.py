#! /usr/bin/python
import sys, tweepy, json, string, random
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

def repeat_tweet(tweet, num_tweets):
    j = 22
    for i in range(0, num_tweets):
        try:
            tweet = list(tweet)
            tweet[j] = random.choice(string.ascii_letters)
            tweet = "".join(tweet) 
            api.update_status(tweet)
            i+=1 
        except: 
            pass

def retweet(rt, fav): 
    for tweet in tweepy.Cursor(api.search, q='#MarchDadness #jimmyfallon').items(7):
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

def retweet_user(): 
    for tweet in tweepy.Cursor(api.user_timeline, user_id='267856525').items(50):
        try: 
            tweet.retweet()
            sleep(.5)
        except tweepy.TweepError as e: 
            print(e.reason)
        except StopIteration: 
            break

def follow(): 
    for tweet in tweepy.Cursor(api.search, q='@kanyewest').items(550): 
        try: 
            if not tweet.user.following:
                tweet.user.follow()
                print("Followed the user")
        except tweepy.TweepError as e: 
            print(e.reason)
        except StopIteration:
            break

if __name__ == '__main__': 

    auth = tweepy.OAuthHandler("sL2BOOaip5M1GZxY9wVJenrtz", "sKrE6ONhuxFE2c1YpaI5BdiDp53N6HL8ILVvubIkbqWQqLMXrh") 
    auth.set_access_token("840213704021049345-X6wFF3URAXSju75ejwY3StLfgtqDIeO", "1XB36ErfJe71f4VnQbrvYVGeVTetKPUwi72VoiBu6HTBo") 
    api = tweepy.API(auth)
    #tweet = "Why did Mozart sell his chickens? Because they all went Bach Bach Bach!"
    tweet = '''Q: What do you call a lost nun?
    #A: A roamin' Catholic.'''
    num_tweets = 100
    repeat_tweet(tweet, num_tweets)
    #file_tweets()
    #retweet(1, 0)
    #follow()
    #retweet_user()



