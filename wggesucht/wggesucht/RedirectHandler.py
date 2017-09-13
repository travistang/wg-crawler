import scrapy
# from scrapy.mail import MailSender
from scrapy.exceptions import IgnoreRequest
import logging
from random import choice,shuffle
import settings
from . import DatasetBroker
import re

class RedirectHandler(object):

	def get_random_proxy(self):
		return self.proxies.next()

	def process_request(self,request,spider):
		# add with proxy if theres not any..
		# do not rotate proxy when it is going to send message
		if 'nachricht-senden' in request.url:
			return
		# no proxies for crawling proxy list...
		if 'sslproxies.org' in request.url:
			return
		#  gather list of proxies if there isnt any
		if not hasattr(self,'proxies'):
			self.proxies = DatasetBroker.DatasetBroker.get_proxy_list()

		request.meta['proxy'] = self.get_random_proxy()
		# return request
		print 'processing request {}, using proxy {}'.format(request.url,request.meta['proxy'])

	def process_response(self,request,response,spider):
		if 'wg-gesucht.de' not in request.url: return response
		if response.status not in [200,303]:
			DatasetBroker.DatasetBroker.add_exception("status {} encountered".format(response.status))
			return response
		return response

	def process_exception(self,request,exception,spider):
		# log the exception
		DatasetBroker.DatasetBroker.add_exception(exception)
		# and rotate proxy and try again
		proxy = self.get_random_proxy()
		new_req = scrapy.Request(request.url,spider.parse)
		new_req.meta['proxy'] = proxy
		return new_req
