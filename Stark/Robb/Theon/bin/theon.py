#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Created on 2017-5-26 by Author:GuoLikai
import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print(BASE_DIR)
sys.path.append(BASE_DIR)

from core import main

if __name__ == '__main__':
    client = main.command_handler(sys.argv)
