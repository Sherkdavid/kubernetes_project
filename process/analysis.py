from textblob import TextBlob
import pika
import json
import re
import time
import redis
'''Consumes a message from the queue'''
def publish(key, value):
    channel.basic_publish(exchange='',
                          routing_key='dbq',
                          body="('"+key+"' , '" + value + "')")
def callback(ch,method,properties,body):
        item = eval(body)
        blob = TextBlob(item[1])
        if blob.polarity ==0:
            publish(item[0],"neutral")
        if blob.polarity >0:
            publish(item[0],"positive")
        if blob.polarity <0:
            publish(item[0],"negative")
if __name__ == "__main__":
    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
    channel = connection.channel(0)
    db = redis.Redis("redis")
    channel.queue_declare(queue='jobq')
    channel.basic_consume(callback, queue='jobq', no_ack=True)
    channel.start_consuming()
