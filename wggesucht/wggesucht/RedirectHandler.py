import scrapy
# from scrapy.mail import MailSender
from scrapy.exceptions import IgnoreRequest
import logging
from random import choice,shuffle
import settings
from . import DatasetBroker
import re

class RedirectHandler(object):
	def __init__(self):
		with open('proxy_list') as pf:
			proxies = map(lambda l: l.replace('\n',''),pf.readlines())
			shuffle(proxies)
			self.proxies = iter(proxies)

	def get_random_proxy(self):
		prox = self.proxies.next()
		print prox
		return prox

	def process_request(self,request,spider):
		# add with proxy if theres not any..
		# do not rotate proxy when it is going to send message
		if 'nachricht-senden' in request.url:
			return
		# check if the ads has been seen before
		try:
			# check if there are ids in the request url
			# if yes then its requesting an ad, check if it has been seen before
			# otherwise let it go
			id = re.search(r'[0-9]{6,7}',request.url).group(0)
			if DatasetBroker.DatasetBroker.is_ad_seen({'ad':id}):
				raise IgnoreRequest()
		except Exception as e:
			# let the IgnoreRequest exception passes through, so the request will be ignored..
			if type(e) == IgnoreRequest:
				raise e

		print 'processed'

		request.meta['proxy'] = self.get_random_proxy()
		# return request
		print 'processing request {}, using proxy {}'.format(request.url,request.meta['proxy'])

	def process_response(self,request,response,spider):
		return response

	def process_exception(self,request,exception,spider):
		proxy = self.get_random_proxy()
		new_req = scrapy.Request(request.url,spider.parse)
		new_req.meta['proxy'] = proxy
		return new_req
