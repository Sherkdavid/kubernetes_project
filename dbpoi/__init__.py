import pika
import json
import re
import time
import redis
'''Consumes a message from the queue'''
def callback(ch,method,properties,body):
        item = eval(body)
        node = db.get(item[0])
        if node == None:
            db.set(item[0], (0,0,0))
            node = db.get(item[0])
        node = eval(node.decode("utf-8"))        
        if item[1] == "positive":
            db.set(item[0], (node[0]+1,node[1],node[2]))
        if item[1] == "negative":
            db.set(item[0], (node[0],node[1]+1,node[2]))
        if item[1] == "neutral":
            db.set(item[0], (node[0],node[1],node[2]+1))
        
if __name__ == "__main__":
    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
    channel = connection.channel(0)
    db = redis.Redis("redis")
    channel.queue_declare(queue='dbq')
    channel.basic_consume(callback, queue='dbq', no_ack=True)
    channel.start_consuming()

