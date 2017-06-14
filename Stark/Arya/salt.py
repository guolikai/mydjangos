#/usr/bin/env python
# -*- coding:utf-8 -*-
#Created on 2017-5-5 by Author:GuoLikai

import os,sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Stark.settings")
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #print(BASE_DIR)
    sys.path.append(BASE_DIR)
    from Arya.action_list import actions
    from Arya.backends.utils import ArgvManagement
    obj = ArgvManagement(sys.argv)