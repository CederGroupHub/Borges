#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import argparse

import requests
from DBGater.db_singleton_mongo import SynDevAdmin
from bs4 import BeautifulSoup
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

__author__ = 'Ziqin (Shaun) Rong'
__maintainer__ = 'Ziqin (Shaun) Rong'
__email__ = 'rongzq08@gmail.com'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", type=str, help="ECS journal name, one of EEL, JES, JSS, SSL")
    args = parser.parse_args()

    db = SynDevAdmin.db_access()
    db.connect()
    issue_col = db.collection('{}_issue'.format(args.j))

    for doc in issue_col.find({"Scraped": False}):
        res = requests.get(doc["URL"])
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'lxml')
            abstract_links = []
            for article in soup.select('.toc-cit'):
                abstract_link = article.find_all('a', {'rel': 'abstract'})
                if abstract_link:
                    abstract_links.append(urljoin(doc["URL"], abstract_link[0].get('href')))
            issue_col.update({"_id": doc["_id"]}, {"$set": {"Scraped": True, "Abstract_Links": abstract_links}})
            print("Scraped Year {}, Issue {}".format(doc['Year'], doc['Issue']))
        else:
            print("Year {}, Issue {} is not scraped successfully".format(doc['Year'], doc["Issue"]))