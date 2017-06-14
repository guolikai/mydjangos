#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Created on 2017-5-26 by Author:GuoLikai
from core import client

class command_handler(object):
    def __init__(self,sys_args):
        self.sys_args = sys_args
        if len(self.sys_args) <2:
            exit(self.help_msg())
        self.command_allowcator()

    def command_allowcator(self):
        '''分拣用户输入的不同指令'''
        print(self.sys_args[1])
        if hasattr(self,self.sys_args[1]):
            func = getattr(self,self.sys_args[1])
            return func()
        else:
            print("Command does not exist!")
            self.help_msg()
    def help_msg(self):
        valid_commands = '''
        start start monitor client
        stop stop monitor client
        '''
        exit(valid_commands)

    def start(self):
        print("Going to start monitor client(core/main.py)")
        #exit_flag = False
        Client = client.ClientHandle()
        Client.forever_run()

    def stop(self):
        print("stopping to the monitor client")