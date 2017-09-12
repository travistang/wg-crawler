# -*- coding: utf-8 -*-
import scrapy


class ProxySpider(scrapy.Spider):
    name = 'proxy'
    allowed_domains = ['sslproxies.org']
    start_urls = ['https://sslproxies.org/']

    def parse(self, response):
        ips = response.xpath('//*[@id="proxylisttable"]/tbody/tr/td[position() = 1]/text()').extract()
        ports = response.xpath('//*[@id="proxylisttable"]/tbody/tr/td[position() = 2]/text()').extract()
        with open('proxy_list','w+') as f:
        	for ip,port in zip(ips,ports):
        		f.writelines('https://{}:{}\n'.format(ip,port))

