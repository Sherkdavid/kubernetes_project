import time
import feedparser

#refresh every 5 minutes
refresh_time = 5*60
if __name__ == '__main__':
    bbc_wn_url = "http://feeds.bbci.co.uk/news/world/rss.xml"
    print("RSS: Scanning at startup ["+bbc_wn_url+"]")
    feed = feedparser.parse(bbc_wn_url)
    print("RSS: "+bbc_wn_url+" scan successful")
    items = []
    for item in feed['items']:
        items.append(item['summary'])

    #scan forever
    while True:
        # sleep for 5 minutes and check for new entries
        time.sleep(refresh_time)
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