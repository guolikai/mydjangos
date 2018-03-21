#!/usr/bin/env python3

import threading
import time
import datetime
import threading 
import os,sys,subprocess
#import commands  #用于python2
import re
#Today=datetime.datetime.now().strftime("%Y-%m-%d")
Today = datetime.date.today()
Yesterday = Today - datetime.timedelta(days=1)
#print(Today,Yesterday)

class MyThread(threading.Thread):
    def __init__(self,func,args=()):
        super(MyThread,self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result 
        except Exception:
            return None

class LinuxOSCommand(object):
    def __init__(self,command):
        self.command = command
    def LinuxOsCommand(self):
        result=[]
        cmd_res = subprocess.getstatusoutput(self.command)
#        print(cmd_res)    #返回的结果是一个元组
        for item in cmd_res[1].split("\n"):
            result.append(item)
        return result
        
class LinuxMysqlBaseOP(object):
    def __init__(self,host,port,user,password,socket):
        self.host=host
        self.port=port
        self.user=user
        self.password=password
        self.socket=socket
        self.connect="mysql -h%s -P%s -u%s -p%s -S %s" % (self.host,self.port,self.user,self.password,self.socket)
    def MysqlStatus(self):
        ret={}
        cmd_res = subprocess.getstatusoutput("%s -e \"show databases\"| grep -Ev \"Database\" | wc -l" % (self.connect))
        result= cmd_res[1]
        ret['data']=result
        return ret

    def ShowData(self):
        database_list=[]
        cmd_res = subprocess.getstatusoutput("%s -e \"show databases\"| grep -Ev \"Database|information_schema|performance_schema|test\"" % (self.connect))
        for dbname in cmd_res[1].split("\n"):
            database_list.append(dbname)
        return database_list

    
    def SelectData(self,selectSQL):
        result_dict={'host':self.host,'data':''}
#        print("%s -e \"%s\" | grep -v id"  % (self.connect,selectSQL))
        Sql_Res = subprocess.getstatusoutput("%s -e \"%s\" | grep -v id"  % (self.connect,selectSQL))
        sql_res = Sql_Res[1]
        if sql_res =='':
            sql_res = 0
        result_dict['data']=sql_res
        return result_dict


    def InsertData(self,InsertSQL):
        result_dict={'host':self.host,'data':''}
        Sql_Res = subprocess.getstatusoutput("%s -e \"%s\""  % (self.connect,InsertSQL))
        sql_res = Sql_Res[1]
        if sql_res =='':
            sql_res = 0
        result_dict['data']=sql_res
        return result_dict

    
    def UpdateData(self,UpdateSQL):
        result_dict={'host':self.host,'data':''}
        Sql_Res = subprocess.getstatusoutput("%s -e \"%s\""  % (self.connect,UpdateSQL))
        sql_res = Sql_Res[1]
        if sql_res =='':
            sql_res = 0
        result_dict['data']=sql_res
        return result_dict

    def DeleteData(self,InsertSQL):
        result_dict={'host':self.host,'data':''}
        Sql_Res = subprocess.getstatusoutput("%s -e \"%s\""  % (self.connect,DeleteSQL))
        sql_res = Sql_Res[1]
        if sql_res =='':
            sql_res = 0
        result_dict['data']=sql_res
        return result_dict
        


if __name__ == '__main__':
    cmd='df -h'
    linuxoscmd = LinuxOSCommand(cmd)
    result = linuxoscmd.LinuxOsCommand()
    print(result)
    print('-------------------------------------------')
    showdb=LinuxMysqlBaseOP('192.168.30.191','3306','analy','analy','/tmp/mysql_3306.sock')
    data_list= showdb.ShowData()
    print(data_list)
    MysqlStatus=showdb.MysqlStatus()['data']
    if MysqlStatus != 0:
        print('Mysql Is UP')
    else:
        print('Mysql Is Down')

