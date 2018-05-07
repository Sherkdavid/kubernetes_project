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
        db.lpush(item[0],(time.time(), blob.polarity))

if __name__ == "__main__":
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel(0)
    db = redis.Redis("redis")
    channel.queue_declare(queue='jobq')
    channel.basic_consume(callback, queue='jobq', no_ack=True)
    channel.start_consuming()
