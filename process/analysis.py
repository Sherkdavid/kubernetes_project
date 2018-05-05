from textblob import TextBlob
import pika
import json
import re
import time
import redis
'''Consumes a message from the queue'''
def callback(ch,method,properties,body):
        #only use an english corpus at the moment so we filter here for english language tweet
        item = eval(body)
        blob = TextBlob(item[1])
        #0's have a pretty massive effect on polarity
        if db.get(item[0])!= None:
            entry = eval(db.get(item[0]))
            entry['hits'] = (entry['hits']+1)
            entry['polarity'] = (entry['polarity'] +blob.polarity)
            db.set(item[0], entry)
        else:
            db.set(item[0], {'hits': 1,'polarity' : blob.polarity})

if __name__ == "__main__":
    waiting = True

    while waiting:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            channel = connection.channel(0)
            waiting = False
        except:
            time.sleep(0.5)
    waiting = True
    while waiting:
        try:
            db = redis.Redis("redis")
            db.flushdb()
            waiting = False
        except:
            time.sleep(0.5)
    channel.queue_declare(queue='tweet_stack')
    channel.basic_consume(callback, queue='tweet_stack', no_ack=True)
    channel.start_consuming()
