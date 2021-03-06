#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from __future__ import unicode_literals

from setuptools import setup, find_packages

__author__ = 'Shaun Rong'
__maintainer__ = 'Shaun Rong'
__email__ = 'rongzq08@gmail.com'

if __name__ == "__main__":
    setup(name='Borges',
          version='0.1.0',
          author="Ceder Group",
          license="MIT License",
          packages=find_packages(),
          zip_safe=False,
          install_requires=[
              'PyYAML',
              'bson',
              'scrapy',
              'requests',
              'beautifulsoup4',
              'jsonlines',
              'sqlalchemy',
              'pymongo',
              'DBGater',
              'pytz',
              'elsapy']
          )
