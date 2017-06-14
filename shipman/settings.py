#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Created on 2017-6-10 by Author:GuoLikai
import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print(BASE_DIR)
sys.path.append(BASE_DIR)
#print(sys.path)


template_variables = dict(
    title=u'Docker管理平台',
    name =u'Docker管理平台',
    username="",
)

DATABASES = dict(
    DB='shipman',
    USERNAME='root',
    PASSWORD='123456',
    HOST='172.16.1.101',
    PORT=3306,
)

NODE_LIST = ['node_ip', 'port']

COOKIE_NAME  = "user_id"