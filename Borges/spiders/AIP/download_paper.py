import urllib.parse
import urllib.request
import json
import scrapy
from bs4 import BeautifulSoup

__author__ = 'Zheren Wang'
__maintainer__ = ''
__email__ = 'zherenwang@berkeley.edu'


class AIPIssuesSpider(scrapy.Spider):

    name = "download_paper"
    json_file = "papers_info.json"

    def start_requests(self):
        yield from self.do_login()

    def do_login(self):
        yield scrapy.Request(url='https://aip.scitation.org/action/showLogin',
                             callback=self.handle_login,
                             dont_filter=True)

    def handle_login(self, res):
        login_id = res.xpath('//input[@name="id"]/@value').extract_first()
        yield scrapy.Request(
            url='https://aip.scitation.org/action/doLogin',
            method='POST',
            body=urllib.parse.urlencode({
                'id': login_id,
                'login': 'zherenwang@berkeley.edu',
                'password': 'ML_Text_Mining',
                'loginSubmit': 'Login',
            }),
            headers={
                'content-type': 'application/x-www-form-urlencoded',
            },
            callback=self.start_scraper,
            dont_filter=True
        )

    def start_scraper(self, res):
        welcome_string = res.xpath('//div[@class="welcome"]/span/text()').extract_first().strip()

        if welcome_string != 'Access provided by Ceder Group At Berkeley And Lbl Berkeley':
            raise RuntimeError('Not logged in, cannot start scraping pages.')

        with open("pipline.json", encoding="utf-8") as f1:
            test = json.load(f1)
            for paper in test:
                print(paper['Article_HTML_Link'])
                url = paper['Article_HTML_Link']
                urllib.request.urlretrieve(url, './htm2.txt')
                break
            request = len(test)


        # relevant_journals = {
        #     "AIP Advances": "adv",
        #     "APL Materials": "apm",
        #     "APL Photonics": "app",
        #     "Applied Physics Letters": "apl",
        #     "Applied Physics Reviews": "are",
        #     "Journal of Applied Physics": "jap",
        #     "The Journal of Chemical Physics": "jcp",
        #     "Journal of Physical and Chemical Reference Data": "jpr",
        #     "Journal of Renewable and Sustainable Energy": "rse",
        #     "Magnetism and Magnetic Materials": "mmm",
        # }
        # for full_name, abbr in relevant_journals.items():
        #     request = scrapy.Request(url="https://aip.scitation.org/toc/{}/current".format(abbr), callback=self.parse)
        #     request.meta['Journal'] = full_name
        #     request.meta["Publisher"] = "AIP"
            yield None


if __name__ == "__main__":
    with open("pipline.json", encoding="utf-8") as f1:
        test = json.load(f1)
        print(len(test))
        for paper in test:
            print(paper['Article_HTML_Link'])

