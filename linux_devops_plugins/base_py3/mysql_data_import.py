#!/bin/env python3

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

import globalsetting
from mysqldatacollect import CollectMain
from bin.linuxbase import LinuxMysqlBaseOP



class LinuxMysqlImportData(object): 
    pass

def ImportMain():
    InsertDatabase='dbcount'
    InsertHostInfo='app01_hostinfo'
    InsertMysqlInfo='app01_mysqlinfo'
    InsertDatabaseInfo='app01_databaseinfo'
    InsertDatabaseSize='app01_databasesize'
    InsertTableInfo='app01_tableinfo'
    InsertTableCount='app01_tablecount'
    InsertMysqlInfos={1:{'host':'192.168.30.191','port':'3307','user':'root','password':'srtadmin','socket':'/tmp/mariadb_3307.sock'},
           }
    print("-------------Starting-------------")
    for key,value in InsertMysqlInfos.items():
        InsertMysqlHost = value['host']
        InsertMysqlPort = value['port']
        InsertMysqlUser = value['user']
        InsertMysqlPassword = value['password']
        InsertMysqlSocket = value['socket']
        print("[%s %s %s %s %s]数据导入中.........." % (InsertMysqlHost,InsertMysqlPort,InsertMysqlUser,InsertMysqlPassword,InsertMysqlSocket))
        #mysqlconn=LinuxMysqlCommand('192.168.30.191','analy','analy','/tmp/mariadb_3306.sock')
        mysqlconn=LinuxMysqlBaseOP(InsertMysqlHost,InsertMysqlPort,InsertMysqlUser,InsertMysqlPassword,InsertMysqlSocket)
        #Host='1.1.1.1'
        Host='192.168.30.191'
        mysql_port='3307'
        dbname='grafana'
        dbsize='0.58'
        table_name='alert'
        table_count='3'

        select_hostinfo_id="select id from %s.%s where ip='%s';" % (InsertDatabase,InsertHostInfo,Host)
        insert_hostinfo="insert into %s.%s(hostname,ip) value('%s','%s');" % (InsertDatabase,InsertHostInfo,Host,Host)
        
        HostId=mysqlconn.SelectData(select_hostinfo_id)
        if  int(HostId['data'])==0:
            mysqlconn.InsertData(insert_hostinfo)
            Host_Result=mysqlconn.SelectData(select_hostinfo_id)
            HostId=Host_Result
        host_id=HostId['data']
        
        select_mysqlinfo_id="select id from %s.%s where mysql_port='%s' and  mysql_host_id='%s';" % (InsertDatabase,InsertMysqlInfo,mysql_port,host_id)
        insert_mysqlinfo="insert into %s.%s(mysql_port,mysql_host_id) value('%s','%s');" % (InsertDatabase,InsertMysqlInfo,mysql_port,host_id)


        MysqlId=mysqlconn.SelectData(select_mysqlinfo_id)
        if  int(MysqlId['data'])==0:
            mysqlconn.InsertData(insert_mysqlinfo)
            Mysql_Result=mysqlconn.SelectData(select_mysqlinfo_id)
            MysqlId=Mysql_Result
        mysql_id=MysqlId['data']



        select_databaseinfo_id="select id from %s.%s where database_name='%s' and database_mysql_id='%s';" % (InsertDatabase,InsertDatabaseInfo,dbname,mysql_id)
        insert_databaseinfo="insert into %s.%s(database_name,database_mysql_id) value('%s','%s');" % (InsertDatabase,InsertDatabaseInfo,dbname,mysql_id)

        DatabaseId=mysqlconn.SelectData(select_databaseinfo_id)
        if  int(DatabaseId['data'])==0:
            mysqlconn.InsertData(insert_databaseinfo)
            Database_Result=mysqlconn.SelectData(select_databaseinfo_id)
            DatabaseId=Database_Result
        database_id=DatabaseId['data']

        select_databasesize_id="select id from %s.%s where database_info_id='%s' and create_date like '%s%s'" % (InsertDatabase,InsertDatabaseSize,database_id,Yesterday,'%')
        insert_databasesize="insert into %s.%s(database_size,create_date,update_date,database_info_id) value('%s','%s','%s','%s');" % (InsertDatabase,InsertDatabaseSize,dbsize,Yesterday,Today,mysql_id)

        DatabasesizeId=mysqlconn.SelectData(select_databasesize_id)
        if  int(DatabasesizeId['data'])==0:
            mysqlconn.InsertData(insert_databasesize)
            Databasesize_Result=mysqlconn.SelectData(select_databasesize_id)
            DatabasesizeId=Databasesize_Result
        databasesize_id=DatabasesizeId['data']
        
        
        select_tableinfo_id="select id from %s.%s where table_name='%s' and  table_mysql_id='%s' and table_database_id='%s';"  % (InsertDatabase,InsertTableInfo,table_name,mysql_id,database_id)
        insert_tableinfo="insert into %s.%s(table_name,table_database_id,table_mysql_id,table_host_ip) value('%s','%s','%s','%s');" % (InsertDatabase,InsertTableInfo,table_name,database_id,mysql_id,host_id)

        TableId=mysqlconn.SelectData(select_tableinfo_id)
        if  int(TableId['data'])==0:
            mysqlconn.InsertData(insert_tableinfo)
            Table_Result=mysqlconn.SelectData(select_tableinfo_id)
            TableId=Table_Result
        table_id=TableId['data']



        select_tablecount_id="select id from %s.%s where table_info_id='%s' and create_date like '%s%s';" % (InsertDatabase,InsertTableCount,table_id,Yesterday,'%')
        insert_tablecount="insert into %s.%s(table_count,create_date,update_date,table_info_id) value('%s','%s','%s','%s');" % (InsertDatabase,InsertTableCount,table_count,Yesterday,Today,table_id)
        TablecountId=mysqlconn.SelectData(select_tablecount_id)
        if  int(TablecountId['data'])==0:
            mysqlconn.InsertData(insert_tablecount)
            Tablecount_Result=mysqlconn.SelectData(select_tablecount_id)
            TablecountId=Tablecount_Result
        tablecount_id=TablecountId['data']

        print("--------------Ended----------------")
    #test=LinuxOSCommand('df -h')
    #Res=test.linux_os_command()
    #print(Res)


if __name__ == '__main__':
    #Operation = input('\033[35;1m请输入需要执行的操作:\033[0m')
    #Operation=sys.argv[1]
    #if Operation == 'collectmain':
    #        CollectMain()
    #elif Operation == 'importmain':
    #        ImportMain()
    #elif Operation == '':
            ImportMain()
   # else:
    #    print("python3 %s Argv:[collectmain/importmain/analymain]" % sys.argv[0])

