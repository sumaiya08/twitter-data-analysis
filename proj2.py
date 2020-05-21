import tweepy
import csv
import io
import de
import dbconn
from urlextract import URLExtract
from textblob import TextBlob
#I'll be using textblob.sentiment in order to perform the sentiment analysis using the Naive Bayes Classification Algorithm
#Ultimately it will be using naive bayes classification algorithm.
from textblob.sentiments import NaiveBayesAnalyzer

# log in via authentication tokens provided by Twitter
from twitter_authentication1 import consumer_key, consumer_secret, access_token, access_token_secret

# this is for authentication by using OAuthHandler and set_access_token method
# from tweepy with a bunch of codes hidden to us
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# main variables to access twitter 
api = tweepy.API(auth)
searchTerm = input("Enter keyword/hashtag to search about: ")

noOfSearchTerms = int(input("Enter how many tweets to analyze:"))
while(noOfSearchTerms<=0):
	noOfSearchTerms = int(input("Enter how many tweets to analyze (more than zero):"))

#Fire Query to search for specific keywords / hash-tag and store it in a Predefined tuple.
public_tweets = tweepy.Cursor(api.search, q=searchTerm, lang="en" , count = noOfSearchTerms).items(noOfSearchTerms)
# now, I want to search for tweets
print("Tweet Data has been fetched")

# To store the fetched tweets in csv file
sum = 0
count = 0

dbconn.dbInitialize()
print("Writing Tweets to database")
for tweet in public_tweets:
		#Using the TextBlob API to analyze the fetched tweets one by one using NaiveBayesAnalyzer 
	analysis = TextBlob(tweet.text , analyzer=NaiveBayesAnalyzer())
		#Store probability of the sentiments of the current tweet being positive 
	pos = analysis.sentiment.p_pos
        #Store probability of the sentiments of the current tweet being negative
	neg = analysis.sentiment.p_neg
		#subjectivity = analysis.sentiment.subjectivity
        # default value for url
        # if url = None, perform operations on tweet.text to cut off existing url
	url = None

        # to start a separate column for URL
        # split texts into chunks
	words = tweet.text.split()

        # To extract URL from the current tweet, if exists
	link = URLExtract()
        # Find links within a tweet
	urls = link.find_urls(tweet.text)

        # identify link - http / https (http is common denominator for both)
	for word in words:
            #print (word)
		if 'http' in word:
			url = word
                
	tweetWithoutURL = str(tweet.text).split(url, 1)[0]
	#print(type(tweetWithoutURL))
	#print(tweetWithoutURL)
	dbconn.dbInsertion(tweetWithoutURL[0:10],tweetWithoutURL, pos, neg, url, tweet.user.location)
	sum = sum + pos
	count = count + 1
        # print to terminal
        #print (tweet.text)
        #print ('Positive: ', pos)
        #print ('Negative:', neg)
sent =  sum/count*100
print("Positive Sentiment Percent = " + str(round(sent,2)) + "%")
dbconn.dbClose()
print("***Data written to database successfully***")
input("\nHit enter to generate WordCloud")
de.createWordCloud()