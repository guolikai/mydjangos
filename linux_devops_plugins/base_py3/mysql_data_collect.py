#!/bin/env python3

import threading
import time
import datetime
import threading 
import os,sys,subprocess
import re
Today = datetime.date.today()
Yesterday = Today - datetime.timedelta(days=1)
import globalsetting 
from bin.LinuxBaseCommand import MyThread
from bin.LinuxBaseCommand import LinuxOSCommand
from bin.LinuxBaseCommand import LinuxMysqlBaseOP
        

class LinuxMysqlCollectData(object):
    def __init__(self,host,port,user,password,socket):
        self.host=host
        self.port=port
        self.user=user
        self.password=password
        self.socket=socket
        self.connect="mysql -h%s -P%s -u%s -p%s -S %s" % (self.host,self.port,self.user,self.password,self.socket)

    def MysqlDatabase(self):
        database_list=[]
        #cmd_res = subprocess.getstatusoutput("self.connect -e \"show databases\"| grep -Ev \"Database|information_schema|performance_schema|test\"" % (self.host,self.user,self.password,self.socket))
        cmd_res = subprocess.getstatusoutput("%s -e \"show databases\"| grep -Ev \"Database|information_schema|performance_schema|test\"" % (self.connect))
        #cmd_res = cmd_res.readlines()
        for dbname in cmd_res[1].split("\n"):
            #print(dbname)
            database_list.append(dbname)
        return database_list
    
    def MysqlDatabaseSize(self):
#        result={'host':self.host,'data':'','port':self.port,'date':Today}
        result={}
        tmp_dict={}
        database_list=self.MysqlDatabase()
        #print(database_list,type(database_list))
        for i  in list(range(len(database_list))):
            dbname = database_list[i]
            cmd_res = subprocess.getstatusoutput("%s -e \"use information_schema;select concat(round(sum(data_length/1024/1024),2),'MB') as data from tables where table_schema=\'%s\'\" | grep -v data"  % (self.connect,dbname))
            for size in cmd_res[1].split("\n"):

                if size=='NULL':
                   size = 0
                tmp_dict[dbname]=size
        result=tmp_dict
        return result

    def MysqlCount(self,dbname,table):
        first_fields=subprocess.getstatusoutput("%s -e \"desc %s.%s;\" |  grep -v \"Field\" | head -1 | awk '{print $1}'"  % (self.connect,dbname,table))
        field=first_fields[1]
        #print("self.connect  -e \"select count(%s) from %s.%s\" | grep -v \"count\""  % (self.host,self.user,self.password,self.socket,field,dbname,table))
        table_counts=subprocess.getstatusoutput("%s -e \"select count('%s') from %s.%s\" | grep -v \"count\""  % (self.connect,field,dbname,table))
        count=table_counts[1]
        return count

    def MysqlSqlCommand(self,sqlcommand):
        result_dict={'host':self.host,'data':''}
        print("%s -e \"%s"  % (self.connect,sqlcommand))
        Sql_Res = subprocess.getstatusoutput("%s -e \"%s\" | grep -v id"  % (self.connect,sqlcommand))
        sql_res = Sql_Res[1]
        result_dict['data']=sql_res
        return result_dict


    def MysqlTableCounts(self):
        #result={'host':self.host,'data':'','port':self.port,'date':Today}
        result={}
        tmp_count_dict={}
        database_list=self.MysqlDatabase()
        for i  in list(range(len(database_list))):
            dbname = database_list[i]
            tmp_table_dict={}
            tables = subprocess.getstatusoutput("%s -e \"use '%s';show tables\" | grep -v \"Tables_in\""  % (self.connect,dbname))
            Len=len(tables)			
    #        print('---------%s'  % Len )
            #t = threading.Thread(target=self.MysqlCount,args=(dbname,table))
            #t.start
            #t.join()
            #startime = time.time()
            #mythread=MyThread()
            List = []
            for table in tables[1].split("\n"):
                if table=='NUll' or table=='':
                    continue
                t = MyThread(self.MysqlCount,args=(dbname,table))
                List.append(t)
                t.start()
    #            print(len(List)) 
                for t in List:
                    t.join()  
                    count = t.get_result()
                    if int(count)==0:
                        continue
                #count=self.MysqlCount(dbname,table)
                    tmp_table_dict[table]=count
                #endtime = time.time()
                #print(endtime - startime)
            #print(len(tmp_table_dict))
            tmp_count_dict[dbname]=tmp_table_dict
        result=tmp_count_dict
        return result



def CollectMain():
    MysqlInfos={1:{'host':'192.168.30.191','port':'3306','user':'analy','password':'analy','socket':'/tmp/mariadb_3306.sock'},
                2:{'host':'192.168.30.191','port':'3307','user':'analy','password':'analy','socket':'/tmp/mysql_3307.sock'},
    #            3:{'host':'10.10.20.220',  'port':'3306','user':'analy','password':'analy','socket':'/tmp/mariadb_3306.sock'},
           }
    print("-------------Starting-------------")
    All_Result={}
    for key,value in MysqlInfos.items():
        MysqlHost = value['host']
        MysqlPort = value['port']
        MysqlUser = value['user']
        MysqlPassword = value['password']
        MysqlSocket = value['socket']
        print("[%s %s %s %s %s]数据收集中.........." % (MysqlHost,MysqlPort,MysqlUser,MysqlPassword,MysqlSocket))
        #mysqlconn=LinuxMysqlCommand('192.168.30.191','analy','analy','/tmp/mariadb_3306.sock')
        CollectData={'host':MysqlHost,'port':MysqlPort,'user':MysqlUser,'socket':MysqlSocket}
        CollectData['collectdatadate']= '%s'  % Yesterday
        CollectData['currentdate']= '%s'  % Today
        mysqlconn=LinuxMysqlCollectData(MysqlHost,MysqlPort,MysqlUser,MysqlPassword,MysqlSocket)
        Size_Result=mysqlconn.MysqlDatabaseSize()
        CollectData['sizedata']=Size_Result
        Count_Result=mysqlconn.MysqlTableCounts()
        CollectData['countdata']=Count_Result
        Host_info = '%s_%s' % (MysqlHost,MysqlPort)
        All_Result[Host_info]= CollectData
    f=open('/root/test.txt','a')
    f.write(str(All_Result))
    f.write('\n')
    print("--------------Ended----------------")
    return All_Result


if __name__ == '__main__':
    Num = len(sys.argv)               #获取命令行的参数
    if Num==1:
        CollectMain()
    else:
        OPS=sys.argv[1]
        if OPS == 'collectmain':
           CollectMain()
        else:
           print("python3 %s Argv:[collectmain]" % sys.argv[0])

