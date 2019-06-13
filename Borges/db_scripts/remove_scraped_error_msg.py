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
    parser.add_argument("-c", type=str, help="collection name where error messages are removed from scraped items")
    args = parser.parse_args()

    db = SynDevAdmin.db_access()
    db.connect()
    col = db.collection(args.c)

    for doc in col.find():
        if doc['Scraped'] and 'Error_Msg' in doc.keys():
            col.update({'_id': doc['_id']}, {'$unset': {'Error_Msg': ""}})
            print("Removed Error_Msg.")

