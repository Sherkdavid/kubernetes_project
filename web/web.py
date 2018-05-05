from flask import Flask
import time
import redis
import json
app = Flask(__name__)


@app.route('/')
def app_home():
    #host = service name
    db = redis.Redis("redis")
#    test = db.lrange('p',start=str(now),end=str(time.asctime(time.localtime(time.time()-600))))
#    print(test)
    text = ""
    for key in db.keys():
        text+=str(key)+" "+str(db.get(key).decode())
    return text


if __name__ == '__main__':
    app.run(host="0.0.0.0")

