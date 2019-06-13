#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import argparse

from DBGater.db_singleton_mongo import SynDevAdmin
from elsapy.elsclient import ElsClient
from elsapy.elssearch import ElsSearch

from Borges.settings import ELSEVIER_API_1, ELSEVIER_API_2, ELSEVIER_API_3, ELSEVIER_API_4

__author__ = 'Ziqin (Shaun) Rong'
__maintainer__ = 'Ziqin (Shaun) Rong'
__email__ = 'rongzq08@gmail.com'


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", type=int, required=True, help="API key number")
    args = parser.parse_args()

    db = SynDevAdmin.db_access()
    db.connect()
    journal_col = db.collection("ElsevierJournals")
    paper_col = db.collection("ElsevierPapers_Update")

    api_keys = {
        1: ELSEVIER_API_1,
        2: ELSEVIER_API_2,
        3: ELSEVIER_API_3,
        4: ELSEVIER_API_4,
    }
    client = ElsClient(api_keys[args.n])

    while True:
        doc = journal_col.find_one({"Journal_Title": "Physics Letters A"})
        if not doc:
            break
        print("Searching for papers from {}".format(doc["Journal_Title"].encode('utf-8')))

        paper_l = []
        scraped_doc_num = 0
        missed_doc_num = 0

        for year in range(2000, 2018):
            doc_search = ElsSearch('ISSN({}) AND YEAR(={})'.format(doc["Journal_ISSN"], year), 'scidir')
            search_success = True
            try:
                doc_search.execute(client, get_all=True)
            except:
                search_success = False

            if search_success:
                for res in doc_search.results:

                    paper_sum = dict()
                    try:
                        paper_sum["Published_Year"] = int(res[u'prism:coverDate'][-1][u'$'].encode("utf-8").split('-')[0])
                    except:
                        paper_sum["Published_Year"] = None

                        paper_sum["Publisher"] = "Elsevier"

                    try:
                        paper_sum["Open_Access"] = bool(int(res[u'openaccess'].encode("utf-8")))
                    except:
                        paper_sum["Open_Access"] = False

                    try:
                        paper_sum["DOI"] = res[u'dc:identifier'].encode("utf-8")
                    except:
                        paper_sum["DOI"] = None

                    try:
                        paper_sum["Title"] = res[u'dc:title'].encode("utf-8")
                    except:
                        paper_sum["Title"] = None

                    try:
                        paper_sum["Authors"] = ["{} {}".format(ath[u'given-name'].encode("utf-8"),
                                                               ath[u'surname'].encode("utf-8"))
                                                for ath in res[u'authors'][u'author']]
                    except:
                        paper_sum["Authors"] = None
                    try:
                        paper_sum["Issue"] = int(res[u'prism:issueIdentifier'].encode("utf-8"))
                    except:
                        paper_sum["Issue"] = None
                    paper_sum["Journal"] = doc["Journal_Title"]

                    if paper_sum["DOI"]:
                        paper_l.append(paper_sum)
                        scraped_doc_num += 1
                    else:
                        missed_doc_num += 1
        if paper_l:
            paper_col.insert_many(paper_l)
        journal_col.update({"_id": doc["_id"]}, {"$set": {"Crawled": True,
                                                          # "Scraped_Doc": doc['Scraped_Doc'] + scraped_doc_num,
                                                          # "Missed_Doc": doc["Missed_Doc"] + missed_doc_num
                                                          }})
        print("Scraped {} papers, missed {} papers from {}.".format(scraped_doc_num, missed_doc_num,
                                                                    doc["Journal_Title"].encode('utf-8')))
