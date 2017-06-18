#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Created on 2017-6-10 by Author:GuoLikai

'''对管理节点的2375端口做些curl操作'''
import os
import pycurl
import json
from io import BytesIO

class Curl(object):
    def __init__(self, curl):
        self.__curl__ = curl

    def get_value(self):
        d_url = pycurl.Curl()
        url_buf = BytesIO()
        d_url.setopt(d_url.URL, self.__curl__)

        try:
            d_url.setopt(d_url.WRITEFUNCTION, url_buf.write)
            d_url.perform()
        except pycurl.error as error:
            errno, errstr = error
            print('An error occurred: ', errstr)
        ret_json = json.loads(url_buf.getvalue().decode())
        return ret_json

    def post_value(self, action, param):
        pass