import os
import tweepy

twitter_consumer_key = os.environ['TWITTER_CONSUMER_KEY']
twitter_consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
twitter_access_token = os.environ["TWITTER_ACCESS_TOKEN"]
twitter_access_secret = os.environ["TWITTER_ACCESS_SECRET"]

auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
auth.set_access_token(twitter_access_token, twitter_access_secret)
api = tweepy.API(auth)


def upload_tweet_with_image(text, image_path):
    """Upload tweet with image"""
    api.update_status_with_media(text, image_path)
