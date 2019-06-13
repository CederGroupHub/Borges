#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import requests
from DBGater.db_singleton_mongo import SynDevAdmin
import time
from pymongo.errors import DocumentTooLarge

from Borges.settings import ELSEVIER_API_1, ELSEVIER_API_2, ELSEVIER_API_3, ELSEVIER_API_4

__author__ = 'Ziqin (Shaun) Rong'
__maintainer__ = 'Ziqin (Shaun) Rong'
__email__ = 'rongzq08@gmail.com'


def scrape_paper(wait_time, col, api_key):
    time.sleep(wait_time)
    doc = col.find_one({"Crawled": False})
    if not doc:
        return 1

    print('Start Scraping for Paper {}.'.format(doc['DOI']))

    res = requests.get("https://api.elsevier.com/content/article/doi/{}?apikey={}&view=FULL".format(doc['DOI'],
                                                                                                    api_key))
    if res.status_code == 200:
        try:
            paper_col.update({'_id': doc["_id"]}, {"$set": {"Paper_Content": res.content, "Crawled": True,
                                                            "Crawled_2": True}})
            print("Successfully Download Paper {}.".format(doc["DOI"]))
        except DocumentTooLarge:
            paper_col.update({'_id': doc['_id']}, {"$set": {"Error": "pymongo.errors.DocumentTooLarge",
                                                            "Crawled": True,
                                                            "Crawled_2": True}})
            print("Document Too Large Error for Paper {}".format(doc['DOI']))
    elif res.status_code == 400:
        paper_col.update({'_id': doc['_id']}, {"$set": {"Error": "Bad Request Code",
                                                        "Crawled": True,
                                                        "Crawled_2": True}})
        print("Bad request URL for Paper {}".format(doc['DOI']))
    else:
        print("Response Code: {}.".format(res.status_code))

    return 0


if __name__ == '__main__':
    db = SynDevAdmin.db_access()
    db.connect()
    paper_col = db.collection("ElsevierPapers")

    while True:
        continue_l = []
        for api in [ELSEVIER_API_1, ELSEVIER_API_2, ELSEVIER_API_3, ELSEVIER_API_4]:
            for i in range(3):
                continue_l.append(scrape_paper(0.1, paper_col, api))
        if sum(continue_l) > 0:
            break
