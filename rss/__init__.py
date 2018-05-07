import time
import feedparser
import pika

def publish(x):
    channel.basic_publish(exchange='',
                          routing_key='jobq',
                          body="('rss' , '" + x + "')")


#refresh every x minutes
refresh_time = 10*60
verbose = True
if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel(0)
    channel.queue_declare(queue='jobq')
    bbc_wn_url = "http://feeds.bbci.co.uk/news/world/rss.xml"
    if verbose:
        print("RSS: Scanning at startup ["+bbc_wn_url+"]")
    feed = feedparser.parse(bbc_wn_url)
    if verbose:
        print("RSS: "+bbc_wn_url+" scan successful")
    items = []
    for item in feed['items']:
        items.append(item['summary'])
        publish(item['summary'])

    #scan forever
    while True:
        # sleep then check for new entries
        time.sleep(refresh_time)
        if verbose:
            print("RSS : Scanning for new entries ["+bbc_wn_url+"]")
        feed = feedparser.parse(bbc_wn_url)
        #fresh scan of items
        fresh = []
        for item in feed['items']:
            fresh.append(item['summary'])
        #discard old entries
        items = [x for x in fresh if items.__contains__(x)]
        #iterate over fresh and add/publish unseen entries
        for item in fresh:
            if not items.__contains__(item):
                items.append(item)
                publish(item)
                if verbose:
                    print("RSS [New] :" +item)