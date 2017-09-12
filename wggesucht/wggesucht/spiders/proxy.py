# -*- coding: utf-8 -*-
import scrapy
from .. import DatasetBroker

class ProxySpider(scrapy.Spider):
    name = 'proxy'
    allowed_domains = ['sslproxies.org']
    start_urls = ['https://sslproxies.org/']

    def parse(self, response):
        ips = response.xpath('//*[@id="proxylisttable"]/tbody/tr[contains(string(),"elite proxy")]/td[position() = 7][contains(string(),"yes")]/parent::tr/td[position() = 1]/text()').extract()
        ports = response.xpath('//*[@id="proxylisttable"]/tbody/tr[contains(string(),"elite proxy")]/td[position() = 7][contains(string(),"yes")]/parent::tr/td[position() = 2]/text()').extract()
        # with open('../wggesucht/wggesucht/proxy_list','w+') as f:
        for ip,port in zip(ips,ports):
            addr = 'https://{}:{}\n'.format(ip,port)
            yield {'ip':ip,'port':port}
