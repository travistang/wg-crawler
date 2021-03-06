# -*- coding: utf-8 -*-
import scrapy
import json
import urllib
import re # for extracting dates
from scrapy.selector import Selector
from datetime import date,datetime # for parsing tenant available time
import datetime
from scrapy import FormRequest
import codecs
from random import choice
import time
import os
from .. import settings
from .. import DatasetBroker
class OfferSpider(scrapy.Spider):
    name = 'offer'
    allowed_domains = ['www.wg-gesucht.de']
    field_or_value = lambda n,v: settings.INFO[n] if n in settings.INFO else v
    url = 'http://www.wg-gesucht.de/en/wg-zimmer-in-Muenchen.90.0.1.0.html?offer_filter=1&sort_column=0&city_id=90&category=0&rent_type={}&rMax={}&wgSea={}&wgAge={}&sin=1&exc=2'.format(
                field_or_value('RENT_TYPE',0),
                field_or_value('MAX_RENT',''),
                field_or_value('GENDER',0),
                field_or_value('AGE',''))

    start_urls = [url]

    @staticmethod
    def field_or_value(n,v):
        return settings.INFO[n] if n in settings.INFO else v


    def parse(self, response):
        sel = Selector(response)
        res = sel.xpath('//div[@id="main_content"]//div[re:test(@id,"liste-details-ad-[0-9]+")]//a[@class="detailansicht"]/@href').extract()
        # now get the url to each of the ads
        # and check whether it has been visited before

        # get some unique ad lists
        ad_lists = reduce(lambda l,r: l if r in l else l + [r],res,[])
        for r in ad_lists:
            yield {'ad_url': r}
    @classmethod
    def ad_parse(cls,response):
        # 1. get the renter's name..
        # BUG: this one will not work starting from September because the name field of the landlord has changed to images...
        # name = sel.xpath('//div[contains(@class,"rhs_contact_information")]//div[contains(@class,"text-capitalise")]/b/text()').extract_first()
        # first_name = HumanName(name.encode('ascii','replace')).first
        this_url = response.url
        # 2. get availablity
        if not cls.is_date_in_criteria(response):
            return

        # proceed to sending message
        id = re.search(r'[0-9]{6,7}',this_url).group(0)
        # log the ad id so it wont be visited again
        yield {'ad':id}
        # prepare form input
        msg_url = "https://www.wg-gesucht.de/en/nachricht-senden.html?id={}".format(id)
        request = scrapy.Request(msg_url,method = 'GET',callback = cls.msg_page,errback = DatasetBroker.DatasetBroker.add_exception)
        yield request

    @classmethod
    def msg_page(cls,response):
        '''
            You needa write something about yourself to send the letters to landlords...
        '''
        assert settings.INFO['LETTER']
        form_data = {
            'nachricht':settings.INFO['LETTER'],
            'u_anrede' : '1',
            'vorname' : OfferSpider.field_or_value('FIRST_NAME',''),
            'nachname' : OfferSpider.field_or_value('LAST_NAME',''),
            'email': OfferSpider.field_or_value('EMAIL',''),
            'telefon':OfferSpider.field_or_value('PHONE',''),
            'agb':"on",
            'kopieanmich':"on",
            'typ':"0",
            'ad_id_val':"",
        }
        # your letters wont be sent if "DONT_SEND" is True
        if settings.INFO['DONT_SEND'] or False:
            print 'didnt send something...'
        else:
            print 'sending letters now...'
            yield scrapy.FormRequest.from_response(response,formname = 'msg_form',formdata = form_data,errback = DatasetBroker.DatasetBroker.add_exception)

    # functions for dealing with some specific infos of pages
    @classmethod
    def is_date_in_criteria(cls,response):
        start_date = response.xpath('//*[@id="main_column"]/div[1]/div/div[3]/div[3]/p/b[1]/text()').extract_first()
        end_date = response.xpath('//*[@id="main_column"]/div[1]/div/div[3]/div[3]/p/b[2]/text()').extract_first()

        to_date = lambda s: datetime.strptime(s,'%d.%m.%Y')
        start_date_lowerbound = OfferSpider.field_or_value('MOVE_IN_DATE_EARLIEST','1.1.1970')
        start_date_upperbound = OfferSpider.field_or_value('MOVE_IN_DATE_LATEST','1.1.2100')
        end_date_lowerbound   = OfferSpider.field_or_value('MOVE_OUT_DATE_EARLIEST','1.1.1970')
        end_date_upperbound   = OfferSpider.field_or_value('MOVE_OUT_DATE_LATEST','1.1.2100')
        try:
            if not (to_date(start_date_lowerbound) <= to_date(start_date) <= to_date(start_date_upperbound)): return False # too late, i will be living under the bridge..
            if not (to_date(end_date_lowerbound) <= to_date(end_date) <= to_date(end_date_upperbound)): return False
            return True
        except:
            # some of them are just not date...
            # do nothing... just keep going
            return True
