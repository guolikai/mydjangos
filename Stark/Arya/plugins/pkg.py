#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Created on 2017-5-5  by Author:GuoLikai

from Arya.backends.base_module import BaseSaltModule

class Pkg(BaseSaltModule):

    def is_required(self,*args,**kwargs):
        #print('--Checking pkg require',args,kwargs)
        cmd = "rpm -qa | grep %s -q;echo $?" % args[1]
        return cmd