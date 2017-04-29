#!/usr/bin/python

# Leah Plofchan, Erin Flynn, Brynna Conway
# Social Sensing and Cyber Physical Systems Final Project
# Twitter Bot Detector Class

import tweepy, sys, json, re, time, datetime, numpy
from textblob import TextBlob
import math
import nltk

class BotDetector():
	def __init__(self, api):
		self.api = api
		self.score = 0
			
	def find_ratio(self, userID):
		# find ratio of followers/following
		user = self.api.get_user(userID)
		#print(user.screen_name)
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
			#print "Point added for follower:friend ratio"
			ratio_score = 100
		elif (ratio1 >= 1.05 and ratio1 < 1.15) or (ratio2 >= 1.05 and ratio2 < 1.15):
			ratio_score = 50
		else:
			ratio_score = 0
		weight = .40
		#print("Ratio_score: {}").format(float(weight*ratio_score))
		self.score += float(weight * ratio_score)

	def num_tweets(self, userID, my_tweets):
		count = 0
		for tweet in my_tweets:
			testimonial = TextBlob(unicode(tweet.text))
			#print tweet.text.encode('utf-8')
			#print testimonial.sentiment.subjectivity
			count += 1
		#print count
	
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
		#print "date count", date_count
		if date_count > 30 and date_count <= 40:
			daily_score = 40
		elif date_count > 40 and date_count <= 50:
			daily_score = 60
		elif date_count > 50 and date_count <= 70:
			daily_score = 80
		elif date_count > 70 and date_count <= 90:
			daily_score = 90
		elif date_count > 90: 
			daily_score = 100
		else:
			daily_score = 0
		#print("daily_score: {}").format(float(weight*daily_score))
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
		#print("bio_score: {}").format(weight*bio_score)
		self.score += float(weight * bio_score)

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
		#print entropy
		if entropy < 1: 
			#print("Entropy extra credit of 30")
			self.score += 30
		elif entropy < 3.5: 
			#print("Entropy extra credit of 10")
			self.score += 10


	def verified(self, user_id):
		user = api.get_user(user_id)
		#print user.profile_image_url
		return user.verified

	def photo(self, user_id):
		weight = 0.1
		user = self.api.get_user(user_id)
		if user.profile_image_url == "http://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png":
			photo_score = 100
			#print "User has default photo"
		else:
			photo_score = 0
			#print "User does not have default photo"
		#print("photo_score: {}").format(weight*photo_score)
		self.score += float(weight*photo_score)

	def url(self, user_id):
		tweets = []
		for page in tweepy.Cursor(self.api.user_timeline, user_id = userID, include_rts = True).pages():
			for tweet in page:
				tweets.append(tweet.text)

		url = [".aero", ".asia", ".biz", ".cat", ".com", ".coop", ".edu", ".gov", ".info", ".int", ".jobs", ".mil", ".mobi", ".museum", ".name", ".net", ".org", ".pro", ".tel", ".travel"]
		url_count = 0
		for tweet in tweets:
			url_bool = False
			#print tweet
			for u in url:
				if u in tweet:
					url_bool = True
					break
			if url_bool == True:
				url_count += 1
		#print url_count 
		
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
			print "{}: {}\n".format(cluster_id, clusters[cluster_id])

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
			#print(len(jaccards[centroid]))
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
			while not self.converged(old_centroids, centroids) and runs < 20: # keep looping until algorithm converges
				old_centroids = centroids 
				clusters = self.calc_clusters(centroids, tweets)
				centroids = self.calc_centroids(clusters, tweets)
				runs += 1
			bot = self.calc_outlier(clusters)
			if bot:
				#print("K-Means extra credit of 20")
				self.score += 20
		except Exception as e:
			#print("Error")
			#print(e)
			return

	def run_functions(self, user, tweets):
		self.score = 0
		self.find_ratio(user)
		self.tweets_per_day(user, tweets)
		self.empty_bio(user)
		self.tweet_time_entropy(user, tweets)
		self.photo(user)
		self.calc_kmeans(user, tweets)


def ratelimit_handled(cursor):
	while True: 
		try: 
			yield cursor.next()
		except tweepy.RateLimitError: 
			#print("IN")
			time.sleep(1)

if __name__ == "__main__":
	# set up authentication
	#auth = tweepy.OAuthHandler('OQvy6pyogx5mxHoIHIHXIIOZh', 'CSXM1Z3UYctTmf4DNL0TtPUD4ecE1AOVc4gJPuSsBYUY8mYnIl')
	#auth.set_access_token('3083135683-DER2kEd9yhEbf7qY2q58haf6MJE3yTzXlOaw9rJ', 	'lU8PL9RrGpmhaxqxmasWP6wzYBMHfB1fOw0TZYe71A380')

	auth = tweepy.OAuthHandler('MQfvmonUl6Ma0BqIDZPf8TgV8','PlsljRGIeseuQP8q14QdFdXdxycNoD3mEbobMV7DkZlANwnpWR')
	auth.set_access_token('965192514-d88SjfmStUJ1ydFo3QIFRm6RrH6iyKu7N3X3gz96', 'D1awNzlohgmHVfPw07oeLE2QrVXi4wFKvCeSDinkazvbl')
	# call tweepy API
	api = tweepy.API(auth)
	user_ids = []
	users_dict = {'338430862': "sofiapack",'388634815' : "halpal111",'2348883242': "flabbie007" ,'2168848020':"Katherine", '591523652':"Anna",'2490371418':"Leah's Human Friend",'3299372399':"Botgle", '1591657148':"justtosay", '1641959030':"favthingsbot",'10729632':"everyword",'2497458150':"fuckeveryword", '86391789':"bigbenclock", '2418365564':"autocharts", '3277928935':"mothgenerator", '3327104705':"censusamericans", '2452239750':"phasechase", '840213704021049345':"JJ", '3366974463':"autocompletejok", '226222147':"Mayor Pete", '828092750834708480':"tiredwinningyet", '597673958':"Erin's Human Friend", '3220758997': "Kanye Bot", '618294231': "Grammar Bot", '2718522424': "Brynna's Human Friend"}
	#user_ids = ['338430862','388634815','2348883242','2168848020', '591523652', '2490371418', '3299372399', '1591657148', '1641959030','10729632','2497458150', '86391789','2418365564', '3277928935', '3327104705', '2452239750', '840213704021049345', '3366974463', '226222147', '828092750834708480', '597673958', '3220758997', '618294231', '2718522424']
	for line in open("users.txt"):
		user_ids.append(line.strip())

	tweets = []
	bd = BotDetector(api)
	#print("sofiapack, halpal111, flabbie007, Katherine, Anna Burbank, Leah's Human Friend, botgle, justtosay, favthingsbot, everyword, fuckeveryword, big_ben_clock, autocharts, mothgenerator, censusamericans, phasechase, JJ, Autocompletejok, Mayor Pete, TiredWinningYet, Erin's Human Friend, Kanye Bot, Grammar Police, Brynna's Human Friend")

	for user in user_ids:
		tweets[:] = []
		pages = 0
		try:
			for page in ratelimit_handled(tweepy.Cursor(api.user_timeline, user_id = user, include_rts = True, count=200).pages(6)):
				for tweet in page:
					tweets.append(tweet)
			verified = bd.verified(user)
			if verified:
				continue
			bd.run_functions(user, tweets)
			print("{}:{}").format(user, bd.score)
		except Exception as e:
			pass
			#print(users_dict[user])
			print(e)
