#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#Created on 2017-11-25 by Author:GuoLikai
import global_setting
from base_py3.linux_os_command import LinuxOSCommand

def main(cmd):
    linuxoscmd = LinuxOSCommand(cmd)
    result = linuxoscmd.LinuxOsCommand()
    return result

if __name__ == '__main__':
    cmd = 'df -h'
    res = main(cmd)
    for index,app_id in enumerate(res):
        #print(index,app_id)
        print(app_id)
