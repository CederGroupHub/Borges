#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import argparse
import time

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

from DBGater.db_singleton_mongo import SynDevAdmin

__author__ = 'Ziqin (Shaun) Rong'
__maintainer__ = 'Ziqin (Shaun) Rong'
__email__ = 'rongzq08@gmail.com'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", type=str, help="ECS journal name, one of EEL, JES, JSS, SSL")
    args = parser.parse_args()

    db = SynDevAdmin.db_access()
    db.connect()
    paper_col = db.collection('{}_paper')

    utc = pytz.timezone('UTC')
    est = pytz.timezone('US/Eastern')

    while True:
        now = datetime.utcnow()
        now_utc = utc.localize(now)
        now_est = now_utc.astimezone(est)

        sleep_time = 10 if now_est.weekday() <= 4 else 5
        time.sleep(sleep_time)

        if now_est.weekday() >= 5 or now_est.hour >= 18 or now_est.hour <= 7:
            doc = paper_col.find_one({"Scraped": True, "Paper_HTML_Scraped": False})
            if not doc:
                break
            res = requests.get(doc["Article_HTML_Link"])
            if res.status_code == 200:
                try:
                    soup = BeautifulSoup(res.content, 'lxml')
                    paper_html_str = soup.select('div.article.fulltext-view')[0]
                    paper_col.update({"_id": doc["_id"]}, {"$set": {"Paper_HTML": str(paper_html_str),
                                                                    "Paper_HTML_Scraped": True}})
                    print("Scraped Success")
                except Exception as e:
                    paper_col.update({"_id": doc["_id"]}, {"$set": {"Error_Msg": str(e)}})
                    print("Scraped Failed, error msg {}".format(str(e)))
                    print("Paper: {}".format(doc["Article_HTML_Link"]))
            else:
                print("Scraped Failed, not able to retrieve the web page. HTML status code: {}, Paper URL {}".
                      format(res.status_code, doc["Article_HTML_Link"]))
                paper_col.update({"_id": doc["_id"]}, {"$set": {"Paper_HTML_Scraped": "Server Issue"}})