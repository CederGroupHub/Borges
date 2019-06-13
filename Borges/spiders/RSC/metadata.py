#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import os
import scrapy
import time
import yaml
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup
from random import randint

__author__ = 'Ziqin (Shaun) Rong'
__maintainer__ = 'Ziqin (Shaun) Rong'
__email__ = 'rongzq08@gmail.com'


class RSCAnalystSpider(scrapy.Spider):
    name = "RSC"

    http_user = 'user'
    http_pass = 'userpass'

    with open(os.path.join(os.path.dirname(__file__), 'start_urls.yaml'), 'r') as yf:
        url_yaml = yaml.load(yf)

    start_urls = url_yaml[name]

    common_info = {"Publisher": name}

    exclude_article_types = ["Cover", "Front/Back Matter"]

    def start_requests(self):
        for url in self.start_urls:
            url = str(url)
            yield SplashRequest(url, self.parse, args={'wait': 2})

    def parse(self, response):
        try:
            crawl_results = self.common_info.copy()
            issue_year = self._parse_issue_year(response)
            crawl_results.update(issue_year)
            if issue_year['Published_Year'] >= 2000:
                print("Scraping journal {}, year {}, issue {}".format(issue_year['Journal'],
                                                                      issue_year['Published_Year'],
                                                                      issue_year['Issue']))

                # Crawling
                for article_tab in response.css('div.capsule.capsule--article'):
                    article_type = BeautifulSoup(article_tab.css('span.capsule__context').extract_first(),
                                                 'html.parser').get_text().strip()
                    open_access = bool(article_tab.css("span.capsule__context > img").extract_first())
                    if article_type not in self.exclude_article_types:
                        article_page = article_tab.css('a.capsule__action::attr(href)').extract_first()
                        article_page = response.urljoin(article_page)
                        current_crawl_results = crawl_results.copy()
                        current_crawl_results.update({"Article_Type": article_type, "Open_Access": open_access})
                        request = SplashRequest(article_page, self._parse_article, args={'wait': 4})
                        request.meta['meta_info'] = current_crawl_results
                        yield request

                # Only crawl papers after 2000
                previous_issue = response.css('.article-nav__bar a:nth-child(1)::attr(href)').extract_first()
                if previous_issue:
                    previous_issue = response.urljoin(previous_issue)
                    yield SplashRequest(previous_issue, self.parse, args={'wait': 8})
        except:
            pass

    @staticmethod
    def _parse_issue_year(response):
        try:
            journal = BeautifulSoup(response.css('.page-head__vcenter > span:nth-child(1)').extract_first(),
                                    'html.parser').get_text().strip()
            issue_year_info = str(response.css('#tabissues .h--heading4').extract_first())
            year = int(issue_year_info.split(",")[0][-4:])
            issue = int(issue_year_info.split(",")[1][-2:])
            return {"Published_Year": year, "Issue": issue, 'Journal': journal}
        except:
            pass

    @staticmethod
    def _parse_article(response):
        try:
            title = BeautifulSoup(response.css("div.article__title > h2.capsule__title").extract_first(),
                                  'html.parser').get_text().strip()

            abstract = BeautifulSoup(response.css("div.capsule__text").extract_first(), 'html.parser').get_text().strip()

            item = response.css("div.list__item--dashed")[1]
            doi = BeautifulSoup(item.css('span.list__item-data').extract_first(), 'html.parser').get_text().strip()

            article_html_link = response.css("a.btn-icon--download+.btn--stack::attr(href)").extract_first()
            article_html_link = response.urljoin(article_html_link)
            article_pdf_link = response.css("a.btn-icon--download::attr(href)").extract_first()
            article_pdf_link = response.urljoin(article_pdf_link)

            authors = []
            for author in response.css('label').extract():
                authors.append(BeautifulSoup(author, 'html.parser').get_text().strip())

            results = {"Title": title,
                       "Abstract": abstract,
                       "DOI": doi,
                       "Article_HTML_Link": article_html_link,
                       "Article_PDF_Link": article_pdf_link,
                       "Authors": authors
                       }
            meta_data = response.meta['meta_info']
            results.update(meta_data)
            yield results
        except:
            pass
