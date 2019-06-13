#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import scrapy
from scrapy_splash import SplashRequest

from DBGater.db_singleton_mongo import SynDevAdmin

__author__ = 'Ziqin (Shaun) Rong'
__maintainer__ = 'Ziqin (Shaun) Rong'
__email__ = 'rongzq08@gmail.com'


class RSCPaperSpider(scrapy.Spider):
    name = "RSC_Paper"

    http_user = 'user'
    http_pass = 'userpass'

    db = SynDevAdmin.db_access()
    db.connect()
    col = db.collection('RSC')

    def start_requests(self):
        for doc in self.col.find({'HTML_Crawled': False}):
            request = SplashRequest(doc['Article_HTML_Link'], self.parse, args={'wait': 2})
            request.meta['DOI'] = doc['DOI']
            yield request

    def parse(self, response):
        try:
            html = response.css('div#wrapper').extract_first()
            if html:
                self.col.update({"DOI": response.meta['DOI']}, {'$set': {'HTML_Crawled': True,
                                                                         "Paper_Content_HTML": html}})
            else:
                self.col.update({"DOI": response.meta['DOI']}, {'$set': {'HTML_Crawled': False,
                                                                         'Error_Msg': "HTML string is None"}})
        except Exception as e:
            self.col.update({"DOI": response.meta['DOI']}, {'$set': {'HTML_Crawled': False,
                                                                     'Error_Msg': str(e)}})
