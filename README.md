# Twitter Bot Detector 
###### Brynna Conway, Erin Flynn, Leah Plofchan 

This Twitter Bot Detector aims to solve the problem of malicious bots negatively affecting the Twitter user experience by identifying all bots on Twitter and classifying each bot as benign or malicious. The bot detector was created in python using the Tweepy API. First, the program collects a large set of user IDs from a stream of tweets based on a filter. The user ID is then extracted from the tweet and is passed into the program, which then iterates through eight classifying functions on the users, parsing through the user’s data and tweets. These functions include verified, default photo, tweets per day,
time of tweet entropy, friend/follower ratio, similarity clustering, empty bio, and URL repetition. Once passed through these functions, a score is calculated using a bot scoring algorithm. If classified as a bot, then a boolean value of 0 or 1 is attached to each bot to signify if it was identified as malicious or benign. After this process, the results are output to the screen. With the outputted data, we manually checked if the users identified as bots appeared to be bots on Twitter. During the initial testing stages, we used the results to reevaluate our bot score algorithm to better identify bots in the future. We then repeated the process. Initially, we used our own bot to test the functionality of the program and create the prototypical bot.

### Results

We ran several trials on the bot detector, using the results of each to improve the algorithm. For the final trial, we ran the detector on 460 users, and 100 of these were detected as bots. Based on our manual checking of these results, 47% of the bots were correctly identified as bots. Analysis of these results and further information about the program can be found in the full report. 

