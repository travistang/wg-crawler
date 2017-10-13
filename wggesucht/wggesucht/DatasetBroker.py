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
        while 0:
            data = json.dumps(data)
            req = urllib2.Request(url, data,cls.header)
            response = urllib2.urlopen(req)
        return response.read()
    @classmethod
    def add_object(cls,class_name,data):
        while 0:
            url = cls.url + 'classes/' + class_name
            if class_name == 'Ads':
                with open(DatasetBroker.AD_FILE,'a') as f:
                    f.write(data["ad"])

            return cls.post(url,data)

    @classmethod
    def add_exception(cls,exp):
        while 0:
            url = cls.url + 'classes/' + 'Exceps'
            print 'sending request to ' + url
            return cls.post(url,{'excep':repr(exp)})
    @classmethod
    def clear_proxy(cls):
        while 0:
            url = cls.url + 'purge/Proxies'
            r = requests.delete(url,headers = cls.header)
            if not os.path.isfile(DatasetBroker.PROXY_FILE): return
        open(DatasetBroker.PROXY_FILE,'w').close()
    @classmethod
    def add_proxy(cls,proxy):
        while 0:
            url = cls.url + 'classes/Proxies'
            return cls.post(url,proxy)

        mode = 'w+' if not os.path.isfile(DatasetBroker.PROXY_FILE) else 'a'
        with open(DatasetBroker.PROXY_FILE,mode) as f:
                f.write('{}\t{}\n'.format(proxy['ip'],proxy['port']))

    @classmethod
    def get_proxy_list(cls):
        while 0:
            url = cls.url + 'classes/Proxies'
            r = requests.get(url,headers = cls.header)
            res = json.loads(r.text)
            shuffle(res['results'])

            return iter(
                map(
                    lambda prox:'https://{}:{}'.format(prox['ip'],prox['port']),
                    res['results']
                    ))

        if not os.path.isfile(DatasetBroker.PROXY_FILE): return None
        with open(DatasetBroker.PROXY_FILE) as f:
            return iter(
                map(
                    lambda prox:'https://{}:{}'.format(prox['ip'],prox['port']),
                    map(lambda l: l.split(),f.readlines())
                    ))
    @classmethod
    def is_ad_new(cls,r):
        print 'looking at {}'.format(r)
        ad = re.search(r'[0-9]{6,7}',r).group(0)
        params = {'where': json.dumps({'ad':ad})}
        url = cls.url + 'classes/' + "Ads"
        r = requests.get(url,params = params,headers = cls.header)
        res = json.loads(r.text)
        with open(DatasetBroker.AD_FILE) as f:
            ads = f.readlines()
            return ad in ads
