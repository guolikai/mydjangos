#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Created on 2017-5-26 by Author:GuoLikai

import subprocess

def monitor():
    '''
    sar -n DEV 1 5命令参数解析：
    IFACE：网络接口的名字
    rxpck/s：每秒钟接收的数据包
    txpck/s：每秒钟发送的数据包
    rxbyt/s：每秒钟接收的字节数
    txbyt/s：每秒钟发送的字节数
    rxcmp/s：每秒钟接收的压缩数据包
    txcmp/s：每秒钟发送的压缩数据包
    rxmcst/s：每秒钟接收的多播数据包
    '''
    shell_command = "sar -n DEV 1 5 | grep -v IFACE | egrep 'Average|平均时间'"
    #status, result = subprocess.getstatusoutput(shell_command)
    result = subprocess.Popen(shell_command,shell=True,stdout=subprocess.PIPE).stdout.readlines()
    value_dic = {'status':0,'data':{}}
    for line in result:
        line = line.split()
        nic_name,t_in,t_out = line[1].decode(),line[4].decode(),line[5].decode(),
        value_dic['data'][nic_name] = {'t_in':t_in,'t_out':t_out}
    #print(value_dic)
    return value_dic

if __name__ == '__main__':
    print(monitor())