#!/usr/bin/python
#coding:utf8
#Created on 2018-04-17 by Author:GuoLikai
#Remarks: 用于收集服务器的硬件信息

from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *
import json
#这里为了简化工作，脚本采用纯python的写法，没有采用Fabric的@task修饰器，
#脚本不需要利用fab执行，直接以python的形式执行即可。


env.user='root'
env.password='srt123'
#hosts=['10.10.10.54','10.10.10.49']

info=[]

@task
#这里用到了@task修饰器,限定只有message_task函数对fab命令可见
@parallel(pool_size=2)
def message_task():
    Info={}
    host_info={}
    print yellow("message service will starting...")
    with settings(warn_only=True):
#这里用的with是确保即便发生异常,也将近早执行下面的清理操作；
#一般来说，Python中的with语句多用于执行清理操作(如关闭文件)，因为python打开文件一会的时间是不确定的，
#如果有其他程序试图访问打开的文件会导致问题;
        ip_res = run("ifconfig bond0 | grep inet | grep -v inet6| awk -F' ' '{print $2}'")
        #cmd = local("uptime",capture=True)
        Host = ip_res.split(':')[1]
        kernal = run("uname -r")
        os=run("cat /etc/redhat-release | awk -F' ' '{print $1,$2,$3}'")
        host_info['OS']  = os +"|"+ kernal
        host_info['SN']  = run("dmidecode -s system-serial-number")
        host_info['Model'] = run("dmidecode -t 1| grep 'Product Name' | awk -F':' '{print $2}'")
        host_info['Manufacturer'] = run("dmidecode -t 1| grep 'Manufacturer' | awk -F':' '{print $2}'")
        host_info['CPU'] = run("cat /proc/cpuinfo | grep name | cut -f2 -d: | uniq")
        mem_size = run("cat /proc/meminfo | grep MemTotal | awk -F' ' '{print $2}'")
        host_info['Mem'] = str(int(mem_size)/1024)+'MB'
        host_info['Disk'] = run("fdisk -l | grep Disk | grep '/dev' | awk -F' |,|:' '{print $2,\"|\",$4,$5}'")
        host_info['Net'] = run("ifconfig -a | grep HWaddr | grep -v bond | awk -F' ' '{print $1,$NF}'")
    Info[Host]=host_info
    info.append(Info)
'''
        cmd_output = run("sh /App/script/SRT/message-service/startServer.sh",pty=False)
        if cmd_output.return_code == 0:
            #这里以绿色字体打印结果:为了方便查看脚本执行结果
            print green("message service restart Success!")
'''


def main(hosts):
#    hosts=['10.10.10.54','10.10.10.49']
    for host in hosts:
        env.host_string = host
        print red("正在%s上执行:" % env.host_string)
        message_task()

    return json.dumps(info)

if __name__ == "__main__":
    hosts=['10.10.10.54','10.10.10.49']
    print main(hosts)
