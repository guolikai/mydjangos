#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Created on 2017-5-23 by Author:GuoLikai

import os,sys,platform

#for linux
if platform.system() == "Windows":
    BASE_DIR = '\\'.join(os.path.abspath(os.path.dirname(__file__)).split('\\')[:-1])
    #print(BASE_DIR)
else:
    BASE_DIR = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])
    #print(BASE_DIR)
#print(BASE_DIR)
sys.path.append(BASE_DIR)

from core import HouseStark

if __name__ == '__main__':
    HouseStark.ArgvHandler(sys.argv)