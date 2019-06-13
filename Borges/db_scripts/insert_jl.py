#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import argparse
import json_lines
from DBGater.db_singleton_mongo import SynDevAdmin

__author__ = 'Ziqin (Shaun) Rong'
__maintainer__ = 'Ziqin (Shaun) Rong'
__email__ = 'rongzq08@gmail.com'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", type=str, help='input file path')
    parser.add_argument("-c", type=str, help="collection name where the json line file is inserted")
    args = parser.parse_args()

    db = SynDevAdmin.db_access()
    db.connect()
    col = db.collection(args.c)

    with open(args.i, 'r') as jlf:
        for item in json_lines.reader(jlf):
            col.insert_one(item)
