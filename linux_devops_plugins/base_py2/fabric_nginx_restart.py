#!/usr/bin/python
#coding:utf8

from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *
#这里为了简化工作，脚本采用纯python的写法，没有采用Fabric的@task修饰器，
#脚本不需要利用fab执行，直接以python的形式执行即可。

env.user='root'
env.password='srt123'
hosts=['10.10.10.74','10.10.20.220']

@task
#这里用到了@task修饰器,限定只有nginx_task函数对fab命令可见
def nginx_task():
	print yellow("Nginx Service will starting...")
	with settings(warn_only=True):
#这里用的with是确保即便发生异常,也将近早执行下面的清理操作；
#一般来说，Python中的with语句多用于执行清理操作(如关闭文件)，因为python打开文件一会的时间是不确定的，
#如果有其他程序试图访问打开的文件会导致问题;
	    sudo("ifconfig br0 | grep inet | grep -v inet6| awk -F' ' '{print $2}'")
        sudo("/etc/init.d/nginx reload",pty=False)
        sudo("/etc/init.d/nginx status")
#这里以绿色字体打印结果:为了方便查看脚本执行结果
	print green("Restart Nginx Service Success!")

for host in hosts:
	env.host_string = host
	nginx_task()
