#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import argparse

from DBGater.db_singleton_mongo import SynDevAdmin
from Borges.spiders.ECS.constants import Journal_Names

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
    paper_col = db.collection('{}_paper'.format(args.j))

    for issue in issue_col.find():
        for link in issue['Abstract_Links']:
            paper_doc = {'Publisher': "ECS", "Article_Type": "Research Article",
                         "Abstract_Link": link, "Journal": Journal_Names[args.j],
                         "Publish_Year": issue['Year'], "Issue": issue['Issue'],
                         "Scraped": False}
            paper_col.insert_one(paper_doc)
