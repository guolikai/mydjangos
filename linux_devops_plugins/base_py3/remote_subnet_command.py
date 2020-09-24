#!/usr/bin/env python
# -*- coding: utf8 -*-
# --------------------------------------------------------------
# Name:        remote_subnet_command.py
# Version:     v1.0
# Create_Date：2017-7-29
# Author:      GuoLikai
# Description: "一个网段内远程批量执行命令"
# --------------------------------------------------------------
import paramiko
import sys
import threading
import os
def remote_comm(host,user,pwd,comm):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host,username=user, password=pwd)
    except Exception as e:
        print('%s: Connection Refused' % host)
    else:
        stdin, stdout, stderr = ssh.exec_command(comm)
        out = stdout.read()
        err = stderr.read()
        if out:
            print("【%s】执行命令【'%s'】输出结果:" % (host,comm))
            #print("%s: %s" % (host, out))
            out=out.decode(encoding="utf-8")
            list = out.split('\n')
            for i in range(len(list)):
                print("%s" % (list[i]))
        if err:
            print("【%s】执行命令【'%s'】输出结果:" % (host,comm))
            #print("Error %s: %s" % (host, err))
            err = err.decode(encoding="utf-8")
            list = err.split('\n')
            for i in range(len(list)):
                print("%s" % (list[i]))
    ssh.close()

def main():
#if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: %s IpSubnet/IP 'Command'" % sys.argv[0])
        sys.exit(1)
    comm = sys.argv[2]
    user = 'newnew'
    password = 'newnew#@321'
    if len(sys.argv[1].split('.')) == 3:
        ips = ["%s.%s" % (sys.argv[1],i) for i in range(1,253)]
        for ip  in ips:
            t = threading.Thread(target=remote_comm, args=(ip,user,password,comm))
            t.start()
    elif len(sys.argv[1].split('.')) ==4:
        ip = sys.argv[1]
        remote_comm(ip,user,password,comm)

if __name__ == '__main__':
    main()
