#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Created on 2017-5-5  by Author:GuoLikai
from Arya.backends.base_module import BaseSaltModule

class User(BaseSaltModule):
    def uid(self,*args,**kwargs):
        self.argv_validation('uid',args[0],int)
        cmd = "-u %s" % args[0]
        self.raw_cmds.append(cmd)
        return cmd
    def gid(self,*args,**kwargs):
        self.argv_validation('gid', args[0],int)
        cmd = "-g %s" % args[0]
        self.raw_cmds.append(cmd)
        return cmd
    def shell(self,*args,**kwargs):
        self.argv_validation('shell', args[0],str)
        cmd = "-s %s" % args[0]
        self.raw_cmds.append(cmd)
        return cmd
    def home(self,*args,**kwargs):
        self.argv_validation('home', args[0],str)
        cmd = "-d %s" % args[0]
        self.raw_cmds.append(cmd)
        return cmd
    def name(self, *args, **kwargs):
        self.argv_validation('name', args[0], str)
        cmd = "%s" % args[0]
        self.raw_cmds.append(cmd)
        return cmd
    def password(self, *args, **kwargs):
        username = kwargs.get('section')
        password = args[0]
        cmd = '''echo "%s" | stdin --password  %s''' % (password,username)
        self.single_line_cmds.append(cmd)
        return cmd
    #拼接客户端需要执行的命令："useradd -u 33 -g 33 -d /var/www/html -s /bin/nologin"
    def present(self,*args,**kwargs):
        cmd_list = []
        username = kwargs.get('section')
        #print("raw_cmds: %s" % self.raw_cmds)
        #print("single_line_cmds: %s" % single_line_cmds)
        self.raw_cmds.insert(0,"useradd %s" %  username)
        cmd_list.append(' '.join(self.raw_cmds))
        cmd_list.extend(self.single_line_cmds)
        #print("--->Cmd_list: %s" % cmd_list)
        #print("cmd_list: %s" % cmd_list[0])
        return cmd_list
        
class UbuntuUser(User):
    def password(self, *args, **kwargs):
        username = kwargs.get('section')
        password = args[0]
        cmd =  '''echo "%s:%s"  | sudo chpasswd''' % (username, password)
        self.single_line_cmds.append(cmd)
        return cmd
