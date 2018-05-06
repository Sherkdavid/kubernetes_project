import tweepy
from tweepy import *
from textblob import TextBlob
import re
import os
import threading
import pika
import json
import os
import time
import redis
class MyStreamListener(tweepy.StreamListener):

    def on_connect(self):
        print("Connection Established")

    '''produce message'''
    def on_data(self, raw_data):
        # limit appears to be the only variation case to be handled that comes through the stream
        if not str(raw_data).__contains__('limit'):
            tweet = json.loads(raw_data)
            # if a retweet, we'll access it and get the 'real text' for it
            if 'retweeted_status' in tweet:
                tweet = tweet['retweeted_status']
            # if truncated need to access the extended tweet object
            if 'extended_tweet' in tweet:
                tweet = clean_tweet(tweet['extended_tweet']['full_text'])
            else:
                tweet = clean_tweet(tweet['text'])
            channel.basic_publish(exchange='',
                              routing_key='tweet_stack',
                              body="('twitter' , '"+tweet+"')")

def clean_tweet(tweet):
    '''
    Borrowed regular expression
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


def auth():
    keyfile = open('keys', 'r')

    keys = eval(keyfile.read())
    auth= OAuthHandler(keys['consumer_key'],keys['consumer_secret'])
    auth.set_access_token(key=keys['access_token'],secret=keys['access_secret'])
    return auth

def start_stream():
    #US Trends
    trends = api.trends_place(23424977)
    #get the first time in trends
    trends = trends[0]['trends']
    #get trend name
    track = trends[0]['name']
    #start stream filter
    stream.filter(track=track,async=True)

if __name__ == "__main__":
    #Have to wait for rabbitmq and redis to launch before we start operation
    waiting = True

    #wait for rabbitmq
    while waiting:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            channel = connection.channel(0)
            channel.queue_declare(queue='jobq')
            waiting = False
        except:
            #try again in 0.5 seconds
            time.sleep(0.5)
    waiting = True

    #wait for redis
    while waiting:
        try:
            db = redis.Redis('redis')
            waiting = False
        except:
            #try again in 0.5 seconds
            time.sleep(0.5)

    #start
    api = tweepy.API(auth())
    listener = MyStreamListener(api=api)
    stream = tweepy.Stream(auth=api.auth, listener=listener)
    '''At end maybe have start stream called on a timed repeat to fetch new top trend'''
    start_stream()
