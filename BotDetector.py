#!/usr/bin/python

# Leah Plofchan, Erin Flynn, Brynna Conway
# Social Sensing and Cyber Physical Systems Final Project
# Twitter Bot Detector Class

import tweepy, sys
import time, datetime
from textblob import TextBlob
import math
import nltk
import re

class BotDetector():
	def __init__(self, api):
		self.api = api
		self.score = 0
			
	def find_ratio(self, userID):
		# find ratio of followers/following
		user = self.api.get_user(userID)
		print user.screen_name
		follower_ids = []

		followers = user.followers_count
		#print "followers count: ", followers
		friends = user.friends_count
		#print "friends (number of people following): ", friends
		try:
			ratio1 = float((float(followers)/float(friends)))
			ratio2 = float((float(friends)/float(followers)))
		except ZeroDivisionError:
			ratio1 = followers
			ratio2 = friends
			self.score += 1
		#print "ratio1: ", ratio1
		#print "ratio2: ", ratio2
		if ratio1 < 0.3 or ratio2 < 0.3:
			print "Point added for follower:friend ratio"
			self.score += 1
		elif (ratio1 > 0.95 and ratio1 < 1.05) or (ratio2 > 0.95 and ratio2 < 1.05):
			print "Point added for follower:friend ratio"
			self.score += 1

	def num_tweets(self, userID):
		status = self.api.user_timeline(user_id = userID, include_rts = True, count = 200)
		count = 0
		for page in tweepy.Cursor(self.api.user_timeline, user_id = userID, include_rts = True).pages():
			for tweet in page:
				testimonial = TextBlob(unicode(tweet.text))
				print tweet.text.encode('utf-8')
				print testimonial.sentiment.subjectivity
				count += 1
				#print tweet.text.encode('utf-8')
		print count
	
	def tweets_per_day(self, userID):
		dates = []
		status = self.api.user_timeline(user_id = userID, include_rts = True, count = 200)
		count = 0
		for page in tweepy.Cursor(self.api.user_timeline, user_id = userID, include_rts = True).pages():
			for tweet in page:
				dates.append(tweet.created_at)
		date_count = 0
		for date in dates:
			if (datetime.datetime.now() - date).days < 1:
				date_count += 1
		#print "date count", date_count
		if date_count > 20 and date_count <= 40:
			print "Point added for number of tweets per day"
			self.score += 1
		elif date_count > 40:
			print "2 points added for number of tweets per day"
			self.score += 2

	# if the user's bio is empty, function will return true
	def empty_bio(self, userID):
		user_list = self.api.lookup_users(user_ids = [userID])
		for user in user_list:
			bio = user.description
		if bio == "":
			print "1/2 point added for empty bio"
			self.score += 0.5
			return True
		else:
			return False

	def tweet_time_entropy(self, user_id):
		tweets = []
		for page in tweepy.Cursor(self.api.user_timeline, user_id = userID, include_rts = True).pages():
			for tweet in page:
				t_time = str(tweet.created_at)
				t_time = t_time.split(" ")
				t_time = t_time[1]
				t_time = t_time.split(":")
				t_time = ':'.join(t_time[:2])
				tweets.append(t_time)
		print tweets[2]
		freq_dist = nltk.FreqDist(tweets)
		probs = [freq_dist.freq(l) for l in freq_dist]
		entropy = -sum(p * math.log(p,2) for p in probs)
		print entropy
		return -sum(p * math.log(p,2) for p in probs)

	def verified(self, user_id):
		user = api.get_user(user_id)
		print user.profile_image_url
		if user.verified == True:
			self.score = 0
			print "User is verified"

	def photo(self, user_id):
		user = api.get_user(user_id)
		if user.profile_image_url == "http://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png":
			self.score += 1
			print "User has default photo"
		else:
			print "User does not have default photo"

	'''
	def url(self, user_id):
		tweets = []
		for page in tweepy.Cursor(self.api.user_timeline, user_id = userID, include_rts = True).pages():
			for tweet in page:
				tweets.append(tweet.text)

		url = [".aero", ".asia", ".biz", ".cat", ".com", ".coop", ".edu", ".gov", ".info", ".int", ".jobs", ".mil", ".mobi", ".museum", ".name", ".net", ".org", ".pro", ".tel", ".travel"]
		url_count = 0
		for tweet in tweets:
			url_bool = False
			print tweet
			for u in url:
				if u in tweet:
					url_bool = True
					break
			if url_bool == True:
				url_count += 1
		print url_count 
	'''

		
if __name__ == "__main__":
	# set up authentication
	auth = tweepy.OAuthHandler('OQvy6pyogx5mxHoIHIHXIIOZh', 'CSXM1Z3UYctTmf4DNL0TtPUD4ecE1AOVc4gJPuSsBYUY8mYnIl')
	auth.set_access_token('3083135683-DER2kEd9yhEbf7qY2q58haf6MJE3yTzXlOaw9rJ', 	'lU8PL9RrGpmhaxqxmasWP6wzYBMHfB1fOw0TZYe71A380')

	# call tweepy API
	api = tweepy.API(auth)
	
	#userID = '198933002' # grammar police twitter
	userID = '226222147' # mayor pete's twitter -- giving out the wrong number of statuses
	#userID = '840213704021049345'
	#userID = '3220758997'	# kanye bot
	#userID = '512021172' # idle hours twitter -- should have 130 followers and 1,226 statuses approx. -- everything is correct for this one
	bd = BotDetector(api)
	#bd.find_ratio(userID)
	
	#bd.tweet_time_entropy(userID)
	#bd.num_tweets(userID)
	#bd.tweets_per_day(userID)
	#bd.empty_bio(userID)

	bd.verified(userID)
	bd.photo(userID)

	print "Bot Score: ", bd.score
	if bd.score > 1:
		print ""
		print "This account is most likely a bot."
	else:
		print ""
		print "This account is most likely not a bot."
