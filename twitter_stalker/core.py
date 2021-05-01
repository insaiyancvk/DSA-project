import tweepy
import re
from textblob import TextBlob


class TwitterStalker():
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret) 
        self.auth.set_access_token(self.access_token, self.access_token_secret) 
        
        # calling the api  
        self.api = tweepy.API(self.auth) 

    def check_who_retweeted(self, tweet_id):
        retweets_list = self.api.retweets(tweet_id) 
        all_retweeted = []
        for retweet in retweets_list: 
            name = retweet.user.screen_name
            all_retweeted.append(name) 


        return all_retweeted

    def trim(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\/\/\S+)", " ", tweet).split())

    def get_tweets(self, screen_name, count = 10):
        tweets = self.api.user_timeline(screen_name= screen_name, count=count, tweet_mode="extended")

        tweets = [self.trim(tweet.full_text) for tweet in tweets]
        return tweets

    def get_tweet_sentiments(self, screen_name, count = 10):
        tweets = self.api.user_timeline(screen_name= screen_name, count=count, tweet_mode="extended")

        tweets = [self.trim(tweet.full_text) for tweet in tweets]

        sentiments = [TextBlob(tweet).sentiment.polarity  for tweet in tweets]
        return sentiments

    
