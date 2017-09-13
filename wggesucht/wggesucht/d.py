import time
import datetime
import subprocess
import random
from multiprocessing import Process

def launch_crawler(crawler_name,sleep_time):
    while True:
        # trying to get the current hour...
        # if you wanna disable this, just comment it out and rebuild the image...
        now = datetime.datetime.now()
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
        hours = (now - midnight).seconds / 3600
        if hours < 6: # stop sending anything before 6 am
            continue

        subprocess.call('scrapy crawl {}'.format(crawler_name).split())
        time.sleep(sleep_time)


if __name__ == '__main__':
    p = Process(target=launch_crawler, args =('offer',20)) # launch offer crawler for every 20 seconds
    q = Process(target=launch_crawler, args = ('proxy',300)) # launch proxy crawler for every 5 mins
    q.start()
    time.sleep(20) # let the proxy crawler populate the proxy list first
    p.start() # then we run the offer crawler
