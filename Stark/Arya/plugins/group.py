#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Created on 2017-5-5  by Author:GuoLikai
from Arya.backends.base_module import BaseSaltModule


class Group(BaseSaltModule):

    def gid(self,*args,**kwargs):
        self.argv_validation('gid',args[0],int)
        cmd = '-g %s' % args[0] 
        return cmd
    def present(self,*args,**kwargs):
        groupname = kwargs.get('section')
        #gid = self.gid()
        #print(gid)
        cmd_list = ["groupadd %s" %groupname]
        return cmd_list
        
        
    def is_required(self,*args,**kwargs):
        cmd = r'''if [ `more /etc/group |awk -F":" '{ print $1 }'|grep -w %s -q;then echo $?''' % args[1]
        return cmd

class UbuntuGroup(Group):
    pass