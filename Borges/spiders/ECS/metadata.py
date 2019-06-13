#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import argparse
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

import time
from bs4 import BeautifulSoup

from DBGater.db_singleton_mongo import SynDevAdmin
import requests

__author__ = 'Ziqin (Shaun) Rong'
__maintainer__ = 'Ziqin (Shaun) Rong'
__email__ = 'rongzq08@gmail.com'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", type=str, help="ECS journal name, one of EEL, JES, JSS, SSL")
    args = parser.parse_args()

    db = SynDevAdmin.db_access()
    db.connect()
    paper_col = db.collection('{}_paper'.format(args.j))

    while True:
        time.sleep(5)
        doc = paper_col.find_one({"Scraped": False})
        if not doc:
            break
        res = requests.get(doc["Abstract_Link"])
        if res.status_code == 200:
            try:
                soup = BeautifulSoup(res.content, 'lxml')
                # open access
                open_access_html = soup.select(".oa-article")
                if open_access_html:
                    open_access = True
                else:
                    open_access = False
                # doi
                doi_html = soup.select(".slug-doi")
                doi = doi_html[0].get_text()
                # Title
                title_html = soup.select("#article-title-1")
                title = title_html[0].get_text()
                # Abstract
                abstract_html = soup.select("#abstract-1")
                abstract = abstract_html[0].select("p")[0].get_text()
                # Article PDF Link
                pdf_a_html = soup.find_all("a", {"rel": "view-full-text.pdf"})
                article_pdf_link = urljoin(doc["Abstract_Link"], pdf_a_html[0].get("href"))
                # Authors
                authors_html = soup.select(".name-search")
                authors = []
                for a in authors_html:
                    authors.append(a.get_text())
                # Article HTML Link
                html_a_html = soup.find_all("a", {"rel": "view-full-text"})
                article_html_link = urljoin(doc["Abstract_Link"], html_a_html[0].get("href"))
                paper_col.update({"_id": doc["_id"]}, {"$set": {"Open_Access": open_access,
                                                                "DOI": doi,
                                                                "Title": title,
                                                                "Abstract": abstract,
                                                                "Article_PDF_Link": article_pdf_link,
                                                                "Authors": authors,
                                                                "Article_HTML_Link": article_html_link,
                                                                "Scraped": True}})
                print("Scraped Success")
            except Exception as e:
                paper_col.update({"_id": doc["_id"]}, {"$set": {"Error_Msg": str(e)}})
                print("Scraped Failed, error msg {}".format(str(e)))
                print("Paper: {}".format(doc["Abstract_Link"]))
        else:
            print("Scraped Failed, not able to retrieve the web page.")
