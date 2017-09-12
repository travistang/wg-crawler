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
    url = 'http://www.wg-gesucht.de/en/wg-zimmer-in-Muenchen.90.0.1.0.html?offer_filter=1&sort_column=0&city_id=90&category=0&rent_type={}&rMax={}&wgSea=2&wgAge={}&sin=1&exc=2'.format(
                settings.INFO['RENT_TYPE'] or 0,
                settings.INFO['MAX_RENT'] or '',
                settings.INFO['AGE'] or '')

    start_urls = [url]
    def parse(self, response):
        sel = Selector(response)
        res = sel.xpath('//div[@id="main_content"]//div[re:test(@id,"liste-details-ad-[0-9]+")]//a[@class="detailansicht"]/@href').extract()
        # now get the url to each of the ads
        # and check whether it has been visited before
        # get some unique IDs
        res = list(set(res))
        for r in res:
            id = re.search(r'[0-9]{6,7}',r).group(0)
            yield {'ad':id}
            # TODO: uncomment me to follow the ads...
            yield response.follow(r,self.ad_parse,dont_filter = True)

    def ad_parse(self,response):
        this_url = response.url
        sel = Selector(response)
        # 1. get the renter's name..
        # BUG: this one will not work starting from September because the name field of the landlord has changed to images...
        # name = sel.xpath('//div[contains(@class,"rhs_contact_information")]//div[contains(@class,"text-capitalise")]/b/text()').extract_first()
        # first_name = HumanName(name.encode('ascii','replace')).first

        # 2. get availablity

        if not self.is_date_in_criteria(response):
            return

        # proceed to sending message
        id = re.search(r'[0-9]{7}',this_url).group(0)
        # TODO: remove me
        return
        # prepare form input
        msg_url = "https://www.wg-gesucht.de/en/nachricht-senden.html?id={}".format(id)
        request = scrapy.Request(msg_url,method = 'GET',callback = self.msg_page)
        yield request

    def msg_page(self,response):
        '''
            You needa write something about yourself to send the letters to landlords...
        '''
        assert settings.INFO['LETTER']
        form_data = {
            'nachricht':settings.INFO['LETTER'],
            'u_anrede' : '1',
            'vorname' : settings.INFO['FIRST_NAME'] or "",
            'nachname' : settings.INFO['LAST_NAME'] or "",
            'email': settings.INFO['EMAIL'] or "",
            'telefon':settings.INFO['PHONE'] or "",
            'agb':"on",
            'kopieanmich':"on",
            'typ':"0",
            'ad_id_val':"",
        }
        # your letters wont be sent if "DONT_SEND" is True
        if settings.INFO['DONT_SEND'] or False:
            print 'didnt send something...'
        else:
            print 'send something...'
            exit()
            yield scrapy.FormRequest.from_response(response,formname = 'msg_form',formdata = form_data)

    # functions for dealing with some specific infos of pages
    def is_date_in_criteria(self,response):
        start_date = response.xpath('//*[@id="main_column"]/div[1]/div/div[3]/div[3]/p/b[1]/text()').extract_first()
        end_date = response.xpath('//*[@id="main_column"]/div[1]/div/div[3]/div[3]/p/b[2]/text()').extract_first()

        to_date = lambda s: datetime.strptime(s,'%d.%m.%Y')
        start_date_lowerbound = settings.INFO['MOVE_IN_DATE_EARLIEST'] or '1.1.1970'
        start_date_upperbound = settings.INFO['MOVE_IN_DATE_LATEST'] or '1.1.2100'
        end_date_lowerbound   = settings.INFO['MOVE_OUT_DATE_EARLIEST'] or '1.1.1970'
        end_date_upperbound   = settings.INFO['MOVE_OUT_DATE_LATEST'] or '1.1.2100'
        try:
            if to_date(start_date_lowerbound) < to_date(start_date) < to_date(start_date_upperbound): return # too late, i will be living under the bridge..
            if to_date(end_date_lowerbound) < to_date(end_date) < to_date(end_date_upperbound): return
        except:
            # some of them are just not date...
            # do nothing... just keep going
            return True
