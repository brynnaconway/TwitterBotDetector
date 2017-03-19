#!/usr/local/bin/python

# Leah Plofchan, Erin Flynn, Brynna Conway
# Social Sensing and Cyber Physical Systems Final Project
# Twitter Bot Detector Class

import tweepy, sys
import time

class BotDetector():
	def __init__(self, api):
		self.api = api
			
	def find_ratio(self, userID):
		# find ratio of followers/following
		user = self.api.get_user(userID)
		print user.screen_name
		#follower_ids = []
		'''for page in tweepy.Cursor(self.api.followers, user_id = userID).pages():
			#for follower in page:
			follower_ids.extend(page)
			time.sleep(20)'''  # keep getting a rate limit error for this stuff

		#followers = len(follower_ids)

		followers = len(self.api.followers_ids(userID))
		friends = len(self.api.friends_ids(userID))
		print "followers: ", followers
		print "friends (number of people following): ", friends
		return float((float(followers)/float(friends)))

		# activity level of user -- how often it tweets and how much it likes other tweets
	# analyze screenname of user and bio
	# score function
	# this currently only gives max of 200 tweets because that is the request max -- trying to figure out how to get around this
	def num_tweets(self, userID):
		status = self.api.user_timeline(user_id = userID, include_rts = True, count = 200)
		print "in here"
		count = 0
		for page in tweepy.Cursor(self.api.user_timeline, user_id = userID, include_rts = True).pages():
			for tweet in page:
				count += 1
				#print tweet.text.encode('utf-8')
		print count
	
if __name__ == "__main__":
	# set up authentication
	auth = tweepy.OAuthHandler('OQvy6pyogx5mxHoIHIHXIIOZh', 'CSXM1Z3UYctTmf4DNL0TtPUD4ecE1AOVc4gJPuSsBYUY8mYnIl')
	auth.set_access_token('3083135683-DER2kEd9yhEbf7qY2q58haf6MJE3yTzXlOaw9rJ', 	'lU8PL9RrGpmhaxqxmasWP6wzYBMHfB1fOw0TZYe71A380')

	# call tweepy API
	api = tweepy.API(auth)
	
	#userID = '965192514' # efly5's twitter
	userID = '226222147' # mayor pete's twitter -- giving out the wrong number of statuses
	#userID = '512021172' # idle hours twitter -- should have 130 followers and 1,226 statuses approx. -- everything is correct for this one
	bd = BotDetector(api)
	print(bd.find_ratio(userID))

	bd.num_tweets(userID)
		
		
		
		
		