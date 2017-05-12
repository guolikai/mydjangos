#!/usr/bin/env python
# _*_ coding:utf8 _*_
'''Created on 2016-12-22 @Author:Guolikai'''

def try_int(arg,default):
    try:
        arg = int(arg)
    except Exception as e:
        arg =  default
    return arg