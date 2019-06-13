#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import argparse

import requests
from bs4 import BeautifulSoup
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse
import jsonlines

__author__ = 'Ziqin (Shaun) Rong'
__maintainer__ = 'Ziqin (Shaun) Rong'
__email__ = 'rongzq08@gmail.com'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", type=str, help="ECS journal name, one of EEL, JES, JSS, SSL")
    args = parser.parse_args()

    base_link = "http://" + args.j.lower() + ".ecsdl.org/site/archive/{}.xhtml"
    with jsonlines.open('{}_issue_link.jl'.format(args.j), mode='a') as writer:
        for year in range(2012, 2016):
            year_link = base_link.format(year)
            res = requests.get(year_link)
            if res.status_code != 200:
                print('Not able to crawl year {} issue links.'.format(year))
            else:
                soup = BeautifulSoup(res.content, 'lxml')
                for issue in soup.select('.proxy-archive-by-year-month a'):
                    text = issue.get_text()
                    vol = text.split(',')[0].split()[1]
                    iss = text.split(',')[1].split()[1]
                    link = issue.get('href')
                    sum_dict = {'Volume': vol, "Issue": iss, "URL": urljoin(base_link, link), "Year": year,
                                "Scraped": False}
                    writer.write(sum_dict)
