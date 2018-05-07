from flask import Flask
import time
import redis
import json
app = Flask(__name__)


@app.route('/')
def app_home():
    #host = service name
    db = redis.Redis("redis")
    text = ""
    for key in db.keys():
        text+=str(db.get(key))
    return text


if __name__ == '__main__':
    app.run(host="0.0.0.0")

