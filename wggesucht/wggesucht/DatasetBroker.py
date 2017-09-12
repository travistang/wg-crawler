import urllib
import urllib2
import json
from scrapy import Reuqest
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
    def request_if_ad_is_new(cls,ad):
        url = cls.url + 'classes/' + "Ads?where={}"
        # data = urllib.urlencode(ad)
        data = urllib.urlencode(json.dumps(ad))
        req = urllib2.Request(url.format(data),None,cls.header)
        response = urllib2.urlopen(req)
        print 'response is',response.read()
        if len(response) == 0:
            yield
