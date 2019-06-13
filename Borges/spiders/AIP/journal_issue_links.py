# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup

__author__ = 'Ziqin (Shaun) Rong'
__maintainer__ = 'Ziqin (Shaun) Rong'
__email__ = 'rongzq08@gmail.com'


class AIPIssuesSpider(scrapy.Spider):

    name = "AIP_MetaData"

    def start_requests(self):
        relevant_journals = {
            "AIP Advances": "adv",
            # "APL Materials": "apm",
            # "APL Photonics": "app",
            # "Applied Physics Letters": "apl",
            # "Applied Physics Reviews": "are",
            # "Journal of Applied Physics": "jap",
            # "The Journal of Chemical Physics": "jcp",
            # "Journal of Physical and Chemical Reference Data": "jpr",
            # "Journal of Renewable and Sustainable Energy": "rse",
            # "Magnetism and Magnetic Materials": "mmm",
        }
        for full_name, abbr in relevant_journals.items():
            request = scrapy.Request(url="https://aip.scitation.org/toc/{}/current".format(abbr), callback=self.parse)
            request.meta['Journal'] = full_name
            request.meta["Publisher"] = "AIP"
            yield request

    def parse(self, response):
        vols = response.css(".expander").getall()
        for vol in vols:
            vol_year = BeautifulSoup(vol).get_text().strip()
            vol = int(vol_year.split()[0])
            year = int(vol_year.split()[1][1:-1])
            # print(vol, year)
            if year >= 2000:
                issues = response.css("li.row.js_issue[data-year='{}']".format(year)).getall()
                print(issues)
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

                    request = SplashRequest(url=response.urljoin(issue_link), callback=self.parse_paper_meta)
                    request.meta.update(meta_data)

                    yield request

    def parse_paper_meta(self, response):
        for paper in response.css(".card-cont").getall():
            results = {}
            results.update(
                {
                    "Volume": response.meta['Volume'],
                    "Published_Year": response.meta['Published_Year'],
                    "Issue": response.meta['Issue'],
                    "Journal": response.meta["Journal"],
                    "Publisher": response.meta["Publisher"]
                }
            )
            paper_tab = BeautifulSoup(paper)

            # Open Access
            div_open_access = paper_tab.find('div.open-access')
            span_open_access = div_open_access.find('span.access-text')
            results["Open_Access"] = False
            if span_open_access:
                results["Open_Access"] = True

            # Title
            h4_title = paper_tab.find('h4.hlFld-Title')
            results["Title"] = h4_title.get_text().strip()

            # DOI & Link
            div_title = paper_tab.find('div.art_title.linkable')
            a_link = div_title.find('a')['href']
            results["Article_HTML_Link"] = response.urljoin(a_link)
            results["DOI"] = "/".join(a_link.split("/")[-2:])

            # Authors
            authors_links = paper_tab.find_all('.hlFld-ContribAuthor a')
            authors = []
            for author in authors_links:
                authors.append(author.get_text().strip())
            results["Authors"] = authors

            # PDF Link
            pdf_link = paper_tab.find('.show-pdf')
            results["Article_PDF_Link"] = response.urljoin(pdf_link)

            yield results



