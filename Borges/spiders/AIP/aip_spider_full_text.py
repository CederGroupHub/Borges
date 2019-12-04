# -*- coding: utf-8 -*-
import urllib.parse
import json
import scrapy
from bs4 import BeautifulSoup

__author__ = 'Zheren Wang'
__maintainer__ = 'Zheren Wang'
__email__ = 'zherenwang@berkeley.edu'


class AIPIssuesSpider(scrapy.Spider):
    name = "aip_spider_full_text"
    json_file = "papers_info.json"

    def start_requests(self):
        yield from self.do_login()

    def start_scraper(self, res):
        welcome_string = res.xpath('//div[@class="welcome"]/span/text()').extract_first().strip()

        if welcome_string != 'Access provided by XXX(account name)':
            raise RuntimeError('Not logged in, cannot start scraping pages.')
        else:
            "gooooooooooood"

        relevant_journals = {
            "AIP Advances": "adv",
            "APL Materials": "apm",
            "APL Photonics": "app",
            "Applied Physics Letters": "apl",
            "Applied Physics Reviews": "are",
            "Journal of Applied Physics": "jap",
            "The Journal of Chemical Physics": "jcp",
            "Journal of Physical and Chemical Reference Data": "jpr",
            "Journal of Renewable and Sustainable Energy": "rse",
            "Magnetism and Magnetic Materials": "mmm",
        }
        for full_name, abbr in relevant_journals.items():
            request = scrapy.Request(url="https://aip.scitation.org/toc/{}/current".format(abbr), callback=self.parse)
            request.meta['Journal'] = full_name
            request.meta["Publisher"] = "AIP"
            yield request

    def handle_login(self, res):
        login_id = res.xpath('//input[@name="id"]/@value').extract_first()
        yield scrapy.Request(
            url='https://aip.scitation.org/action/doLogin',
            method='POST',
            body=urllib.parse.urlencode({
                'id': login_id,
                'login': 'Your AIP Username',
                'password': 'Your AIP Password',
                'loginSubmit': 'Login',
            }),
            headers={
                'content-type': 'application/x-www-form-urlencoded',
            },
            callback=self.start_scraper,
            dont_filter=True
        )

    def do_login(self):
        yield scrapy.Request(url='https://aip.scitation.org/action/showLogin',
                             callback=self.handle_login,
                             dont_filter=True)

    def parse(self, response):
        vols = response.css(".expander").getall()
        for vol in vols:
            vol_year = BeautifulSoup(vol).get_text().strip()
            vol = int(vol_year.split()[0])
            year = int(vol_year.split()[1][1:-1])
            # print(vol, year)
            if year >= 2018:
                issues = response.css("li.row.js_issue[data-year='{}']".format(year)).getall()
                for iss in issues:
                    iss = BeautifulSoup(iss)
                    iss_num = iss.li['data-issue']
                    issue_link = iss.find('a')['href']
                    meta_data = {
                        "Volume": vol,
                        "Published_Year": year,
                        "Issue": iss_num,
                        "Journal": response.meta["Journal"],
                        "Publisher": response.meta["Publisher"]
                    }

                    request = scrapy.Request(url="{}?size=all".format(response.urljoin(issue_link)),
                                             callback=self.parse_paper_meta)
                    request.meta.update(meta_data)

                    yield request

    # @staticmethod
    def parse_paper_meta(self, response):
        for paper in response.css(".card-cont"):
            meta_data = {
                "Volume": response.meta['Volume'],
                "Published_Year": response.meta['Published_Year'],
                "Issue": response.meta['Issue'],
                "Journal": response.meta["Journal"],
                "Publisher": response.meta["Publisher"]
            }

            # Open Access
            div_open_access = paper.css('div.open-access')[0]
            span_open_access = div_open_access.css('span.access-text').extract_first()
            meta_data["Open_Access"] = False
            if span_open_access:
                meta_data["Open_Access"] = True

            # Title
            h4_title = paper.css('h4.hlFld-Title').extract_first()
            meta_data["Title"] = BeautifulSoup(h4_title).get_text().strip()

            # DOI & Link
            div_title = paper.css('div.art_title.linkable')[0]
            a_link = div_title.css('a::attr(href)').extract_first()
            meta_data["Article_HTML_Link"] = response.urljoin(a_link)
            meta_data["DOI"] = "/".join(a_link.split("/")[-2:])
            # Authors
            authors_links = paper.css('.hlFld-ContribAuthor a').getall()
            authors = []
            for author in authors_links:
                authors.append(BeautifulSoup(author).get_text().strip())
            meta_data["Authors"] = authors

            # PDF Link
            pdf_link = paper.css('.show-pdf::attr(href)').extract_first()
            meta_data["Article_PDF_Link"] = response.urljoin(pdf_link)

            request = scrapy.Request(url=meta_data["Article_HTML_Link"],
                                     callback=self.parse_full_text)
            request.meta.update(meta_data)

            yield request

    @staticmethod
    def parse_full_text(response):

        results = {
            "Volume": response.meta['Volume'],
            "Published_Year": response.meta['Published_Year'],
            "Issue": response.meta['Issue'],
            "Journal": response.meta["Journal"],
            "Publisher": response.meta["Publisher"],
            "Open_Access": response.meta["Open_Access"],
            "DOI": response.meta["DOI"],
            "Title": response.meta["Title"],
            "Article_HTML_Link": response.meta["Article_HTML_Link"],
            "Authors": response.meta["Authors"],
            "Article_PDF_Link": response.meta["Article_PDF_Link"],
            "Full_text": response.xpath('//div[contains(@class,"page-body pagefulltext")]').extract_first().strip()
        }

        yield results
