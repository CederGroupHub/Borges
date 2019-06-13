#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import argparse

from DBGater.db_singleton_mongo import SynDevAdmin

__author__ = 'Ziqin (Shaun) Rong'
__maintainer__ = 'Ziqin (Shaun) Rong'
__email__ = 'rongzq08@gmail.com'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", type=str, help="collection name where the progress is inspected")
    args = parser.parse_args()

    db = SynDevAdmin.db_access()
    db.connect()
    col = db.collection(args.c)

    scraped_doc = 0
    all_doc = 0
    for doc in col.find():
        if doc['Paper_HTML_Scraped']:
            scraped_doc += 1
        elif doc['Paper_HTML_Scraped'] == "Server Issue":
            print("Doc {} not able to scrape due to server issue.".format(doc['Article_HTML_Link']))
        all_doc += 1

    print("All Doc: {}, Scraped Doc: {}, Scraped {}%.".format(all_doc, scraped_doc, float(scraped_doc) / all_doc * 100))
