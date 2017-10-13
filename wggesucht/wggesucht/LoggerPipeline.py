from scrapy.exceptions import DropItem
import scrapy
import urllib
import urllib2
import json
from . import DatasetBroker
import re
from spiders import offer as O
class LoggerPipeline(object):
    # internal class for storing database object defs...
    # structs for storing ads
    def __init__(self, crawler):
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def open_spider(self, spider):
        pass

    def query_object(self,class_name,**args):
        pass
    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if 'ad' in item:
            # the item is an ad...
            DatasetBroker.DatasetBroker.add_object("Ads",item)
            return item
        elif 'ad_url' in item:
            # check if the item should be followed...
            aid = re.search(r'[0-9]{6,7}',item['ad_url']).group(0)
            if DatasetBroker.DatasetBroker.is_ad_new(aid):
                self.crawler.engine.crawl(
                    scrapy.Request(
                        url = 'https://www.wg-gesucht.de/{}.html'.format(aid),
                        callback = O.OfferSpider.ad_parse,
                        errback = DatasetBroker.DatasetBroker.add_exception),
                spider)
                return item
        elif 'ip' in item:
            DatasetBroker.DatasetBroker.add_proxy(item)
            return item
        else:
            raise DropItem('Ignoring item {}'.format(item))
