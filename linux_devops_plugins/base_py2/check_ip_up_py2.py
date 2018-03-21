#!/usr/bin/env python
# -*- coding: utf8 -*-
# --------------------------------------------------------------
# Name:        check_ip_up.py
# Version:     v1.0
# Create_Date：2017-7-29
# Author:      GuoLikai
# Description: "确认IP是否UP"
# --------------------------------------------------------------

import subprocess  # 该模块用于调用系统命令
import threading
import sys

def ping(ip):
    result = subprocess.call(
        'ping -c2 %s &> /dev/null' % ip, shell=True
    )  # result的结果是ping的退出码
    if result == 0:
        print "%s:up" % ip
    else:
        print "%s:down" % ip

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: %s ip-subnet" % sys.argv[0]
        sys.exit(1)
    subnet = sys.argv[1]
    ips = ["%s.%s" % (subnet,i) for i in range(1, 255)]
    for ipaddr in ips:
        t = threading.Thread(target=ping, args=[ipaddr])
        t.start()
