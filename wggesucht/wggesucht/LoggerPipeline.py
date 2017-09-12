from scrapy.exceptions import DropItem

import urllib
import urllib2
import json
from . import DatasetBroker
class LoggerPipeline(object):
    # internal class for storing database object defs...
    # structs for storing ads

    def open_spider(self, spider):
        pass

    def query_object(self,class_name,**args):
        pass
    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if item['ad']:
            # the item is an ad...
            DatasetBroker.DatasetBroker.add_object("Ads",item)
            return item
        raise DropItem('Ignoring item {}'.format(item))

    # This should directly be called by RedirectHandler
