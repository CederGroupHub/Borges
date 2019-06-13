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
    parser.add_argument("-i", type=str, help="collection from where the docs will be inserted")
    parser.add_argument("-o", type=str, help='collection to where the docs will be inserted')
    args = parser.parse_args()

    db = SynDevAdmin.db_access()
    db.connect()
    col_from = db.collection(args.i)
    col_to = db.collection(args.o)

    for doc in col_from.find():
        doc['Published_Year'] = doc['Publish_Year']
        del doc['Publish_Year']
        del doc['Scraped']
        doc['HTML_Crawled'] = doc['Paper_HTML_Scraped']
        del doc['Paper_HTML_Scraped']
        if doc['HTML_Crawled'] == True:
            doc['Paper_HTML_content'] = doc['Paper_HTML']
            del doc['Paper_HTML']
        col_to.insert_one(doc)
