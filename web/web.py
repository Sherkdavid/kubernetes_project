from flask import Flask
import time
import redis
import json
app = Flask(__name__)


def getResultForKey(key):
    #get all entries stored in (time, polarity) tuple
    entries = db.lrange(key,0,-1)
    polarity = 0.0
    i = 0.0
    for entry in entries:
        polarity+=float(eval(entry.decode("utf-8"))[1])
        i+=1
    #return str(entries)
    return "Instances>"+str(i)+" Polarity>"+str(polarity)

def getRes(key):
    node = db.get(key)
    node = eval(node.decode("utf-8"))
    return "Positive :" + str(node[0]) + " Negative :"+str(node[1])+" Neutral :"+str(node[2])
            

@app.route('/')
def app_home():
    text = "<h1>Polarity of data sources</h1>"
    for key in db.keys():
        text+=str(key)+ " : " + getRes(key)+"<br>"
    return text


if __name__ == '__main__':
    db = redis.Redis("redis")        
    app.run(host="0.0.0.0")
