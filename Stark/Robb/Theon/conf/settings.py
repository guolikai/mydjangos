#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Created on 2017-5-26 by Author:GuoLikai

configs = {
    'HostID':1,
    'Server':'172.16.1.68',
    'ServerPort':8000,
    'urls':{
        'get_configs':['monitor/api/client/config','GET'],
        'service_report':['monitor/api/client/service/report/','POST']
    },
    'RequestTimeout':30,
    'ConfUpdateInterval':300, #5min as default;
}