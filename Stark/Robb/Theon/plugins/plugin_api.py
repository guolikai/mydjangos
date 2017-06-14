#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Created on 2017-5-26 by Author:GuoLikai

from plugins.linux import load,cpu_mac,cpu,memory,network
#from plugins.linux import host_alive

def LinuxSysInfo():
    return sysinfo.collect()

def WindowsSysInfo():
    from windows import sysinfo as win_sysinfo
    return win_sysinfo.collect()

#def host_alive_check():
#    return host_alive.monitor()

def GetMacCPU():
    #return cpu.monitor()
    return cpu_mac.monitor()

def GetLinuxNetworkStatus():
    return network.monitor()

def GetLinuxMemoryStatus():
    return memory.monitor()

def GetLinuxCpuStatus():
    return cpu.monitor()

