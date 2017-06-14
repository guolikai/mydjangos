#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Created on 2017-5-5  by Author:GuoLikai
from Arya.backends.base_module import BaseSaltModule


class File(BaseSaltModule):

    def managed(self,*args,**kwargs):
        #print('\033[33;1mmanaged.m\033[0m',args,kwargs)
        kwargs['sub_action'] = 'managed'
        self.data['file_source'] = True
        return kwargs
    def user(self,*args,**kwargs):
        pass
    def group(self,*args,**kwargs):
        pass
    def mode(self,*args,**kwargs):
        pass
    def is_required(self,*args,**kwargs):
        #print('file  require',args,kwargs)
        file_path = args[1]
        cmd = r'''test -f %s; echo $?'''  %  file_path
        return cmd
    def directory(self,*args,**kwargs):
        kwargs['sub_action'] = 'directory'
        return self.managed(*args,**kwargs)
    def source(self,*args,**kwargs):
        #print('source:',args,kwargs)
        return [args[0]]
    def sources(self,*args,**kwargs):
        #print('sources:',args,kwargs)
        return args[0]
    def recurse(self,*args,**kwargs):
        pass