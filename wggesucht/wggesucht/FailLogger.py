from scrapy import signals
from . import DatasetBroker
class FailLogger(object):

  @classmethod
  def from_crawler(cls, crawler):
    ext = cls()

    crawler.signals.connect(ext.spider_error, signal=signals.spider_error)

    return ext

  def spider_error(self, failure, response, spider):
    print "Error on {0}, traceback: {1}".format(response.url, failure.getTraceback())
    DatasetBroker.DatasetBroker.add_exception(repr(failure))
