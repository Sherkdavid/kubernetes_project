from flask import Flask
import time
import redis
import json
app = Flask(__name__)


def getResultForKey(key):
    #get all entries stored in (time, polarity) tuple
    entries = db.lrange(key,0,-1)
    now = time.time()
    i=0
    trim = False
    for entry in entries:
        if entry[0] > (now - (1000*5*60)):
            i+=1
        if entry[0] < (now - (1000*5*60)):
            trim = True
    #if trim:
    #    db.ltrim(key,0,i)
    recent = db.lrange(key,0,i)
    polarity = 0
    items = len(recent)
    for item in recent:
        polarity+=item[1]
    return entries
            

@app.route('/')
def app_home():
    #host = service name
    text = "<h1>Polarity of data sources in the last 5 minutes</h1>"
    for key in db.keys():
        text+=str(key)+ " AVG Polarity : " + str(getResultForKey(key))+"<br>"
    return text


if __name__ == '__main__':
    db = redis.Redis("redis")        
    app.run(host="0.0.0.0")

