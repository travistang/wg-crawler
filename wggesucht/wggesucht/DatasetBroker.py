import urllib
import urllib2
import json
from scrapy.exceptions import IgnoreRequest
import re
import os
import requests
from random import shuffle

class DatasetBroker(object):
    url = "http://parse-server:1337/parse/"
    header = {
    "X-Parse-Application-Id": "wggesucht",
    "X-Parse-Master-Key": "wggesucht",
    "Content-Type": "application/json",
    }
    PROXY_FILE = "proxy_list"
    AD_FILE = "ad_list"
    @classmethod
    def post(cls,url,data):
        pass
    @classmethod
    def add_object(cls,class_name,data):
        print 'writing...'
        with open(DatasetBroker.AD_FILE,'a') as f:
            f.write("{}\n".format(data["ad"]))

    @classmethod
    def add_exception(cls,exp):
        pass
        
    @classmethod
    def clear_proxy(cls):
        open(DatasetBroker.PROXY_FILE,'w').close()
    @classmethod
    def add_proxy(cls,proxy):
        mode = 'w+' if not os.path.isfile(DatasetBroker.PROXY_FILE) else 'a'
        with open(DatasetBroker.PROXY_FILE,mode) as f:
                f.write('{}\t{}\n'.format(proxy['ip'],proxy['port']))

    @classmethod
    def get_proxy_list(cls):
        if not os.path.isfile(DatasetBroker.PROXY_FILE): return None
        with open(DatasetBroker.PROXY_FILE) as f:
            proxies = f.readlines()
            shuffle(proxies)
            return iter(
                map(
                    lambda prox:'https://{}:{}'.format(prox[0],prox[1]),
                    map(lambda l: l.split('\t'),proxies)
                ))
    @classmethod
    def is_ad_new(cls,r):
        if not os.path.isfile(DatasetBroker.AD_FILE):
            open(DatasetBroker.AD_FILE,'a').close()
            return True # because not even a single ad has been seen before..
        # extract the id here...
        with open(DatasetBroker.AD_FILE) as f:
            ads = map(lambda l: l.replace('\n','').strip(),f.readlines())
            return r not in ads
