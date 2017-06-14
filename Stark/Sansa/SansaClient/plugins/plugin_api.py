#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Created on 2017-5-23 by Author:GuoLikai

from plugins.linux import sysinfo

def LinuxSysInfo():
    #print __file__
    return  sysinfo.collect()
def WindowsSysInfo():
    from windows import sysinfo as win_sysinfo
    return win_sysinfo.collect()
