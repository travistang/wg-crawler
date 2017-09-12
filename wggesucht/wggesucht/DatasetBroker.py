import urllib
import urllib2
import json
from scrapy.exceptions import IgnoreRequest
import re
import requests
class DatasetBroker(object):
    url = "http://localhost:1337/parse/"
    header = {
        "X-Parse-Application-Id": "wggesucht",
        "X-Parse-REST-API-Key": "wggesucht",
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
    def is_ad_new(cls,r):
        print 'looking at {}'.format(r)
        ad = re.search(r'[0-9]{6,7}',r).group(0)
        params = {'where': json.dumps({'ad':ad})}
        url = cls.url + 'classes/' + "Ads"
        # data = urllib.urlencode(ad)
        r = requests.get(url,params = params,headers = cls.header)
        print r.text
        res = json.loads(r.text)
        return len(res['results']) == 0
        # return len(r.text) == ''
