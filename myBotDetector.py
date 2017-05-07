#!/usr/bin/python

# Leah Plofchan, Erin Flynn, Brynna Conway
# Social Sensing and Cyber Physical Systems Final Project
# Twitter Bot Detector Class

import tweepy, sys, json, re, time, datetime, numpy
from textblob import TextBlob
import math
import nltk
import collections

class BotDetector():
	def __init__(self, api):
		self.api = api
		self.score = 0
			
	def find_ratio(self, userID):
		# find ratio of followers/following
		user = self.api.get_user(userID)
		follower_ids = []

		followers = user.followers_count
		friends = user.friends_count

		try:
			ratio1 = float((float(followers)/float(friends)))
			ratio2 = float((float(friends)/float(followers)))
		except ZeroDivisionError:
			ratio1 = followers
			ratio2 = friends
			self.score += 1
		if ratio1 < 0.1 or ratio2 < 0.1:
			ratio_score = 100		
		elif (ratio1 >= 0.1 and ratio1 < 0.3) or (ratio2 >= 0.1 and ratio2 < 0.3):
			ratio_score = 90
		elif (ratio1 > 0.85 and ratio1 <= 0.95) or (ratio2 > 0.85 and ratio2 <= 0.95):
			ratio_score = 50
		elif (ratio1 > 0.95 and ratio1 < 1.05) or (ratio2 > 0.95 and ratio2 < 1.05):
			ratio_score = 100
		elif (ratio1 >= 1.05 and ratio1 < 1.15) or (ratio2 >= 1.05 and ratio2 < 1.15):
			ratio_score = 50
		else:
			ratio_score = 0
		weight = .40
		self.score += float(weight * ratio_score)

	def num_tweets(self, userID, my_tweets):
		count = 0
		for tweet in my_tweets:
			testimonial = TextBlob(unicode(tweet.text))
			count += 1
	
	# find the number of tweets user posts per day, give score accordingly 
	def tweets_per_day(self, userID, my_tweets):
		dates = []
		count = 0
		weight = .40
		for tweet in my_tweets:
			dates.append(tweet.created_at)
		date_count = 0
		for date in dates:
			if (datetime.datetime.now() - date).days < 1:
				date_count += 1
		if date_count > 60 and date_count <= 70:
			daily_score = 50
		elif date_count > 70 and date_count <= 100:
			daily_score = 70
		elif date_count > 100: 
			daily_score = 100
		else:
			daily_score = 0
		self.score += float(weight * daily_score)

	# if the user's bio is empty, function will return true
	def empty_bio(self, userID):
		user_list = self.api.lookup_users(user_ids = [userID])
		weight = 0.1

		for user in user_list:
			bio = user.description
		if bio == "":
			bio_score = 100
		else:
			bio_score = 0
		self.score += float(weight * bio_score)

	# check for variety of time of tweets 
	def tweet_time_entropy(self, user_id, my_tweets):
		tweets = []
		for tweet in my_tweets:
			t_time = str(tweet.created_at)
			t_time = t_time.split(" ")
			t_time = t_time[1]
			t_time = t_time.split(":")
			t_time = ':'.join(t_time[:2])
			tweets.append(t_time)
		freq_dist = nltk.FreqDist(tweets)
		probs = [freq_dist.freq(l) for l in freq_dist]
		entropy = -sum(p * math.log(p,2) for p in probs)
		if entropy < 1: 
			self.score += 30
		elif entropy < 3.5: 
			self.score += 10


	# if a user is verified, automatically not a bot
	def verified(self, user_id):
		user = api.get_user(user_id)
		self.score = 0
		self.malicious = 0
		return user.verified

	# if a user doesn't have a photo, more likely to be a bot
	def photo(self, user_id):
		weight = 0.1
		user = self.api.get_user(user_id)
		if user.profile_image_url == "http://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png":
			photo_score = 100
		else:
			photo_score = 0
		self.score += float(weight*photo_score)
		
	# K-Means Clustering of tweets to find similarity
	# calculate the jaccard distance between two tweets 
	def calc_jaccard(self, tweet1, tweet2): 
		tweet1 = re.sub(r'[^\w\s]','', tweet1) # remove puncuation
		tweet2 = re.sub(r'[^\w\s]','',tweet2)
		
		t1 = set(tweet1.split())
		t2 = set(tweet2.split())

		intersection = len(t1.intersection(t2))
		union = len(t1.union(t2))
		if union == 0:
			return 1
		jaccard = 1 - (float(intersection)/float(union))
		return jaccard

	# get the new clusters
	def calc_clusters(self, centroids, tweets): 

		clusters = {}
		jaccards = {}
		self.avg_jaccards.clear()

		for id1 in tweets.keys(): # loop through all tweet ids
			the_min = 1 
			min_id = id1
			for id2 in centroids: # find centroid closest to tweet 
				curr = self.calc_jaccard(tweets[id1], tweets[id2])  
				if curr < the_min: # find smallest jaccard distance 
					the_min = curr
					min_id = id2 # note which centroid is closest 
			try:
				clusters[min_id].append(id1) # add tweet to centroid's cluster
			except KeyError: 
				clusters[min_id] = [id1] # create new cluster for this centroid
			try:
				jaccards[min_id].append(the_min)
			except KeyError:
				jaccards[min_id] = [the_min]
		self.calc_avg_jaccard(jaccards)

		return clusters

	# calculate new centroids based on clusters 
	def calc_centroids(self, clusters, tweets):

		new_centroids = [] # list of new centroids 
		for centroid in clusters.keys(): # loop through current centroids
			min_sum = 300
			sum = 0
			min_id = centroid
			for id1 in clusters[centroid]: # find distance between tweet of id1 and all other tweets
				for id2 in clusters[centroid]: # loop through to compare to all tweets
					sum += self.calc_jaccard(tweets[id1], tweets[id2])
				if sum < min_sum:
					min_sum = sum
					min_id = id1
				sum = 0
			new_centroids.append(min_id)
		return new_centroids

	# determine if centroids are no longer changing 
	def converged(self, old_centroids, centroids): 
		return old_centroids == centroids

	def print_clusters(self, clusters,tweets): 
		for cluster_id in clusters.keys():
			print("{}: {}\n".format(cluster_id, clusters[cluster_id]))

	def calc_outlier(self, clusters):
		cluster_sizes = []
		size_dict = {}
		outlier = 0
		for cluster_id in clusters:
			cluster_sizes.append(len(clusters[cluster_id]))
			size_dict[cluster_id] = len(clusters[cluster_id])
		median = numpy.median(cluster_sizes)
		cluster_sizes.sort()
		Q1 = numpy.percentile(cluster_sizes, 25)
		Q3 = numpy.percentile(cluster_sizes, 75)
		IQR = Q3-Q1
		upper = float(IQR*1.5)
		for centroid in size_dict.keys(): 
			if size_dict[centroid] > upper and self.avg_jaccards[centroid] < 0.20:
				outlier = 1
		return outlier

	def calc_avg_jaccard(self, jaccards):

		for centroid in jaccards.keys():
			my_sum = 0
			for jaccard in jaccards[centroid]:
				my_sum += jaccard
			avg = float(my_sum/len(jaccards[centroid]))
			self.avg_jaccards[centroid] = avg

	def calc_kmeans(self, user_id, my_tweets): 
		self.avg_jaccards = {}
		tweets = {} # dict with tweet id as key, text as value 
		clusters = {} # dict with centroid as key, tweets in cluster as values
		centroids = [] # list of centroids 
		old_centroids = None

		try:
			for tweet in my_tweets:
				tweet = tweet._json
				idnum = str(tweet['id']).strip() # sets string id number to id of tweet 
				tweets[idnum] = (tweet['text']) # stores tweets text in dict, with id as key

			# Get initial list of centroids 
			key_nums = len(tweets.keys())
			i = 0
			change = (key_nums/15)
			while i < key_nums:
				id_num = tweets.keys()[i]
				centroids.append(id_num)
				i+=change
			runs = 0
			while not self.converged(old_centroids, centroids) and runs < 15: # keep looping until algorithm converges
				old_centroids = centroids 
				clusters = self.calc_clusters(centroids, tweets)
				centroids = self.calc_centroids(clusters, tweets)
				runs += 1
			bot = self.calc_outlier(clusters)
			if bot:
				self.score += 20
				self.malicious = 1
		except Exception as e:
			return

	# determine if user is tweeting many identical URLs
	def url(self, user_id, tweets):
		count = collections.Counter()
		for tweet in tweets:
			tweet = tweet._json
			try:
				url = tweet["entities"]["urls"][0]["url"]
				count[url] += 1
			except:
				pass
		try:
			ratio = float(len(count.keys()) / sum(count.values()))
			if ratio <= 0.05:
				self.score += 20
				self.malicious = 1
			elif ratio <= .1 and ratio > 0.05:
				self.score += 15
				self.malicious =1
		except:
			return

	# run all of the functions used to compute score 
	def run_functions(self, user, tweets):
		self.score = 0
		self.malicious = 0
		self.find_ratio(user)
		self.tweets_per_day(user, tweets)
		self.empty_bio(user)
		self.tweet_time_entropy(user, tweets)
		self.photo(user)
		self.calc_kmeans(user, tweets)
		self.url(user, tweets)


def ratelimit_handled(cursor):
	while True: 
		try: 
			yield cursor.next()
		except tweepy.RateLimitError: 
			print("IN")
			time.sleep(1)



if __name__ == "__main__":
	# set up authentication

	auth = tweepy.OAuthHandler('MQfvmonUl6Ma0BqIDZPf8TgV8','PlsljRGIeseuQP8q14QdFdXdxycNoD3mEbobMV7DkZlANwnpWR')
	auth.set_access_token('965192514-d88SjfmStUJ1ydFo3QIFRm6RrH6iyKu7N3X3gz96', 'D1awNzlohgmHVfPw07oeLE2QrVXi4wFKvCeSDinkazvbl')
	# call tweepy API
	api = tweepy.API(auth)
	user_ids = []
	for line in open("users2.txt"):
		user_ids.append(line.strip())
	tweets = []
	bd = BotDetector(api)
	for user in user_ids:
		tweets[:] = []
		try:
			verified = bd.verified(user) # check if user is verified 
			if not verified: # run functions to give score to unverified users 
				for page in ratelimit_handled(tweepy.Cursor(api.user_timeline, user_id = user, include_rts = True, count=200).pages(6)):
					for tweet in page:
						tweets.append(tweet)
				bd.run_functions(user, tweets)
			print("{}:{}:{}").format(user, bd.score, bd.malicious)

		except Exception as e:
			pass
			print(e)
