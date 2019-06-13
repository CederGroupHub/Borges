#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import os
import yaml

__author__ = 'Ziqin (Shaun) Rong'
__maintainer__ = 'Ziqin (Shaun) Rong'
__email__ = 'rongzq08@gmail.com'


if __name__ == '__main__':
    with open(os.path.join(os.path.dirname(__file__), '..', 'start_url_gen_params_format_1.yaml'), 'r') as yf1:
        params_1 = yaml.load(yf1)
    with open(os.path.join(os.path.dirname(__file__), '..', 'start_url_gen_params_format_2.yaml'), 'r') as yf2:
        params_2 = yaml.load(yf2)
    start_url = {"RSC": []}
    for k, v in params_1['RSC'].items():
        for vol in range(v['start_vol'], v['end_vol'] + 1):
            for iss in range(1, v['issue_per_year'] + 1):
                vol_issue_str = str(vol).zfill(3) + str(iss).zfill(3)
                start_url['RSC'].append(v['format'].format(vol_issue_str))
    for k, v in params_2['RSC'].items():
        for vol in range(v['start_vol'], v['end_vol'] + 1):
            for iss in range(v['start_issue'], v['end_issue'] + 1):
                vol_issue_str = str(vol).zfill(3) + str(iss).zfill(3)
                start_url['RSC'].append(v['format'].format(vol_issue_str))
    with open(os.path.join(os.path.dirname(__file__), '..', 'start_urls.yaml'), 'w') as yf:
        yaml.dump(start_url, yf, default_flow_style=False)
