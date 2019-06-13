#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from bs4 import BeautifulSoup

import scrapy

__author__ = 'Ziqin (Shaun) Rong'
__maintainer__ = 'Ziqin (Shaun) Rong'
__email__ = 'rongzq08@gmail.com'


class ElsevierJournals(scrapy.Spider):
    name = "Elsevier_Journal"
    start_urls = ["https://www.elsevier.com/catalog?page={}&author=&cat0=27360&cat1=&categoryrestriction=&imprintname=&producttype=journal&q=&sort=datedesc".format(page)
                  for page in range(1, 2)] +\
                 ["https://www.elsevier.com/catalog?page={}&author=&cat0=27360&cat1=&categoryrestriction=&imprintname=&producttype=journal&q=&sort=datedesc".format(page)
                  for page in range(1, 10)] + \
                 ["https://www.elsevier.com/catalog?page={}&author=&cat0=27362&cat1=&categoryrestriction=&imprintname=&producttype=journal&q=&sort=datedesc".format(page)
                  for page in range(1, 10)] + \
                 ["https://www.elsevier.com/catalog?page={}&author=&cat0=27368&cat1=&categoryrestriction=&imprintname=&producttype=journal&q=&sort=datedesc".format(page)
                  for page in range(1, 6)] + \
                 ["https://www.elsevier.com/catalog?page={}&author=&cat0=27370&cat1=&categoryrestriction=&imprintname=&producttype=journal&q=&sort=datedesc".format(page)
                  for page in range(1, 14)] +\
                 ["https://www.elsevier.com/catalog?page={}&author=&cat0=27372&cat1=&categoryrestriction=&imprintname=&producttype=journal&q=&sort=datedesc".format(page)
                  for page in range(1, 7)] + \
                 ["https://www.elsevier.com/catalog?page={}&author=&cat0=27374&cat1=&categoryrestriction=&imprintname=&producttype=journal&q=&sort=datedesc".format(page)
                  for page in range(1, 11)]

    def parse(self, response):
        for journal_tab in response.css(".listing-products"):
            journal_link = journal_tab.css(".listing-products-info-text-title a::attr(href)").extract_first()
            journal_link = response.urljoin(journal_link)

            yield scrapy.Request(journal_link, callback=self._parse_journal_page)

    @staticmethod
    def _parse_journal_page(response):
        journal_summary = {}
        title_html = response.css("h1").extract_first()
        journal_summary["Journal_Title"] = BeautifulSoup(title_html).get_text().strip()

        open_access_html = response.css(".open-access-btn a").extract_first()
        journal_summary["Open_Access"] = (BeautifulSoup(open_access_html).get_text().strip() == "Open Access")

        journal_main_page_link = response.css("a.view-articles::attr(href)").extract_first()
        journal_main_page_link = response.urljoin(journal_main_page_link)
        journal_summary["Journal_Main_Page_Link"] = journal_main_page_link

        yield journal_summary
