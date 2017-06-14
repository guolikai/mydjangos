#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Created on 2017-5-23 by Author:GuoLikai

import os
BaseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

Params = {
    "server": "172.16.1.68",
    "port":8000,
    'request_timeout':30,
    "urls":{
          "asset_report_with_no_id":"/asset/report/asset_with_no_asset_id/",
          "asset_report":"/asset/report/",
        },
    'asset_id': '%s/var/.asset_id' % BaseDir,
    'log_file': '%s/logs/run_log' % BaseDir,

    'auth':{
        'user':'admin@lzhot.net',
        'token': 'test'
        },
}
