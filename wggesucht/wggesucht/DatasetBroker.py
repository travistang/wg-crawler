import urllib
import urllib2
import json
from scrapy.exceptions import IgnoreRequest
import re
import requests
from random import shuffle
class DatasetBroker(object):
    url = "http://localhost:1337/parse/"
    header = {
        "X-Parse-Application-Id": "wggesucht",
        "X-Parse-Master-Key": "wggesucht",
        "Content-Type": "application/json",
    }

    @classmethod
    def post(cls,url,data):
        data = json.dumps(data)
        req = urllib2.Request(url, data,cls.header)
        response = urllib2.urlopen(req)
        return response.read()

    @classmethod
    def add_object(cls,class_name,data):
        url = cls.url + 'classes/' + class_name
        return cls.post(url,data)

    @classmethod
    def add_exception(cls,exp):
        url = cls.url + 'classes/' + 'Exceps'
        print 'sending request to ' + url
        return cls.post(url,{'excep':repr(exp)})

    @classmethod
    def clear_proxy(cls):
        url = cls.url + 'purge/Proxies'
        r = requests.delete(url,headers = cls.header)

    @classmethod
    def add_proxy(cls,proxy):
        url = cls.url + 'classes/Proxies'
        return cls.post(url,proxy)

    @classmethod
    def get_proxy_list(cls):
        url = cls.url + 'classes/Proxies'
        r = requests.get(url,headers = cls.header)
        res = json.loads(r.text)
        shuffle(res['results'])
        return iter(
                    map(
                        lambda prox:'https://{}:{}'.format(prox['ip'],prox['port']),
                        res['results']
                        ))

    @classmethod
    def is_ad_new(cls,r):
        print 'looking at {}'.format(r)
        ad = re.search(r'[0-9]{6,7}',r).group(0)
        params = {'where': json.dumps({'ad':ad})}
        url = cls.url + 'classes/' + "Ads"
        # data = urllib.urlencode(ad)
        r = requests.get(url,params = params,headers = cls.header)
        res = json.loads(r.text)
        return len(res['results']) == 0
        # return len(r.text) == ''
