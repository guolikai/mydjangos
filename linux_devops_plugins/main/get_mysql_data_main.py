#!/bin/env python3
#---------------------------------------------------------------
# Name:        get_mysql_data_main.py
# Version:     v1.0
# Create_Date：2017-11-20
# Author:      GuoLikai(glk73748196@sina.com)
# Description: "Python Collect Import Analy MySQL Data"
#---------------------------------------------------------------
#import commands  #用于python2
import threading
import time
import datetime
import threading 
import os,sys,subprocess
import re
import xlwt
#Today=datetime.datetime.now().strftime("%Y-%m-%d")
Today = datetime.date.today()
Yesterday = Today - datetime.timedelta(days=1)


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
    def __init__(self):
        pass
    def LinuxOsCommand(self,command):
        result=[]
        cmd_res = subprocess.getstatusoutput(command)
#        print(cmd_res)    #返回的结果是一个元组
        if cmd_res[0]==0:
            for item in cmd_res[1].split("\n"):
                result.append(item)
            return result


def LinuxWriteExcelArray(Data,TableName,SaveDirFile):
    workbook=xlwt.Workbook(encoding='utf-8')  
    booksheet=workbook.add_sheet(TableName,cell_overwrite_ok=True)
    for i,row in enumerate(Data):  
        for j,col in enumerate(row):
            booksheet.write(i,j,col)  
    workbook.save('%s' % (SaveDirFile))

def LinuxWriteExcelTwo(Data1,Data2,Table1,Table2,SaveDirFile):
    workbook=xlwt.Workbook(encoding='utf-8')  
    booksheet=workbook.add_sheet(Table1,cell_overwrite_ok=True)
    for i,row in enumerate(Data1):  
        for j,col in enumerate(row):
            booksheet.write(i,j,col)  
    
    booksheet=workbook.add_sheet(Table2,cell_overwrite_ok=True)
    for i,row in enumerate(Data2):  
        for j,col in enumerate(row):
            booksheet.write(i,j,col)  

    workbook.save('%s' % (SaveDirFile))
					

class LinuxMysqlCollectData(object):
    def __init__(self,host,port,user,password,socket):
        self.host=host
        self.port=port
        self.user=user
        self.password=password
        self.socket=socket
        self.connect="mysql -h%s -P%s -u%s -p%s -S %s" % (self.host,self.port,self.user,self.password,self.socket)
        self.adminconn="mysqladmin -h%s -P%s -u%s -p%s -S %s" % (self.host,self.port,self.user,self.password,self.socket)
    def MysqlPing(self,Ping):
        cmd_res = subprocess.getstatusoutput("%s %s|grep alive|wc -l" % (self.adminconn,Ping))
        #print(cmd_res[1])
        if cmd_res[1]=='1':
            return 1
        else:
            return 0

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
#       result={'host':self.host,'data':'','port':self.port,'date':Today}
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
        #print(dbname,table,table_counts)
        count=table_counts[1]
        #print(dbname,table,count)
        return count

    def MysqlSqlCommand(self,sqlcommand):
        result_dict={'host':self.host,'data':''}
        #print("%s -e \"%s"  % (self.connect,sqlcommand))
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
                    #if int(count)==0:
                    #    continue
                #count=self.MysqlCount(dbname,table)
                    tmp_table_dict[table]=count
                #endtime = time.time()
                #print(endtime - startime)
            #print(len(tmp_table_dict))
            tmp_count_dict[dbname]=tmp_table_dict
        result=tmp_count_dict
        return result


class LinuxMysqlBaseOP(object):
    def __init__(self,host,port,user,password,socket):
        self.host=host
        self.port=port
        self.user=user
        self.password=password
        self.socket=socket
        self.connect="mysql -h%s -P%s -u%s -p%s -S %s" % (self.host,self.port,self.user,self.password,self.socket)
    
    def SelectData(self,selectSQL):
        result_dict={'host':self.host,'data':''}
        #print("%s -e \"%s\" | grep -v id"  % (self.connect,selectSQL))
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
        if Sql_Res[0] != 0:
            print('\033[1;31mInput SQL Error:\033[0m',sql_res)
            sql_res = 0
        result_dict['data']=sql_res
        return result_dict

    
    def UpdateData(self,UpdateSQL):
        result_dict={'host':self.host,'data':''}
        Sql_Res = subprocess.getstatusoutput("%s -e \"%s\""  % (self.connect,UpdateSQL))
        sql_res = Sql_Res[1]
        if Sql_Res[0] != 0:
            sql_res = 0
        result_dict['data']=sql_res
        return result_dict

    def DeleteData(self,DeleteSQL):
        result_dict={'host':self.host,'data':''}
        Sql_Res = subprocess.getstatusoutput("%s -e \"%s\""  % (self.connect,DeleteSQL))
        sql_res = Sql_Res[1]
        if Sql_Res[0] != 0:
            sql_res = 0
        result_dict['data']=sql_res
        return result_dict
        

def CollectMain():
    MysqlInfos={1:{'host':'192.168.30.191','port':'3306','user':'analy','password':'analy','socket':'/tmp/mariadb_3306.sock'},
                #2:{'host':'192.168.30.191','port':'3307','user':'analy','password':'analy','socket':'/tmp/mysql_3307.sock'},
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


class LinuxMysqlImportData(object):
    def __init__(self,host,port,user,password,socket):
        self.host=host
        self.port=port
        self.user=user
        self.password=password
        self.socket=socket
        self.connect="mysql -h%s -P%s -u%s -p%s -S %s" % (self.host,self.port,self.user,self.password,self.socket)
        self.mysqlconn=LinuxMysqlBaseOP(self.host,self.port,self.user,self.password,self.socket)
    def HandleSizeData(self,collect_data):
        for key,value in collect_data.items():
           # for key1,value1 in value.items():
                if key=='sizedata':
                    Sizedata=collect_data[key]
        return Sizedata
    
    def HandleCountData(self,collect_data):
        for key,value in collect_data.items():
        ##    for key1,value1 in value.items():
                if key=='countdata':
                    Countdata=collect_data[key]
        return Countdata

    def HandleHostData(self,collect_data):
        for key,value in collect_data.items():
        #    for key1,value1 in value.items():
                if key == 'host':
                    Host=collect_data[key]
        return Host


    def HandlePortData(self,collect_data):
        for key,value in collect_data.items():
        #    for key1,value1 in value.items():
                if key=='port':
                    Port=collect_data[key]
        return Port

    def GetHostId(self,InsertDatabase,InsertHostInfo,Host):
        #mysqlconn=LinuxMysqlBaseOP(self.host,self.port,self.user,self.password,self.socket)
        select_hostinfo_id="select id from %s.%s where ip='%s';" % (InsertDatabase,InsertHostInfo,Host)
        insert_hostinfo="insert into %s.%s(hostname,ip) value('%s','%s');" % (InsertDatabase,InsertHostInfo,Host,Host)
        HostId=self.mysqlconn.SelectData(select_hostinfo_id)
        if  int(HostId['data'])==0:
            self.mysqlconn.InsertData(insert_hostinfo)
            Host_Result=self.mysqlconn.SelectData(select_hostinfo_id)
            HostId=Host_Result
        return HostId['data']
    
    def GetMysqlId(self,InsertDatabase,InsertMysqlInfo,mysql_port,host_id):
        select_mysqlinfo_id = "select id from %s.%s where mysql_port='%s' and  mysql_host_id='%s';" % (InsertDatabase,InsertMysqlInfo,mysql_port,host_id)
        insert_mysqlinfo = "insert into %s.%s(mysql_port,mysql_host_id) value('%s','%s');" % (InsertDatabase,InsertMysqlInfo,mysql_port,host_id)
        MysqlId = self.mysqlconn.SelectData(select_mysqlinfo_id)
        if  int(MysqlId['data']) == 0:
            self.mysqlconn.InsertData(insert_mysqlinfo)
            Mysql_Result = self.mysqlconn.SelectData(select_mysqlinfo_id)
            MysqlId=Mysql_Result
        return MysqlId['data']


    def GetDatabaseInfoId(self,InsertDatabase,InsertDatabaseInfo,mysql_id,dbname):
        select_databaseinfo_id = "select id from %s.%s where database_name='%s' and database_mysql_id='%s';" % (InsertDatabase,InsertDatabaseInfo,dbname,mysql_id)
        insert_databaseinfo = "insert into %s.%s(database_name,database_mysql_id) value('%s','%s');" % (InsertDatabase,InsertDatabaseInfo,dbname,mysql_id)
        DatabaseinfoId = self.mysqlconn.SelectData(select_databaseinfo_id)
        if  int(DatabaseinfoId['data']) == 0:
            self.mysqlconn.InsertData(insert_databaseinfo)
            Databaseinfo_Result = self.mysqlconn.SelectData(select_databaseinfo_id)
            DatabaseinfoId = Databaseinfo_Result
        return DatabaseinfoId['data']

    def GetDatabaseSizeId(self,InsertDatabase,InsertDatabaseSize,database_id,dbsize):
        select_databasesize_id = "select id from %s.%s where database_info_id='%s' and create_date like '%s%s'" % (InsertDatabase,InsertDatabaseSize,database_id,Yesterday,'%')
        insert_databasesize = "insert into %s.%s(database_size,create_date,update_date,database_info_id) value('%s','%s','%s','%s');" % (InsertDatabase,InsertDatabaseSize,dbsize,Yesterday,Today,database_id)
        DatabasesizeId = self.mysqlconn.SelectData(select_databasesize_id)
        if  int(DatabasesizeId['data'])==0:
            self.mysqlconn.InsertData(insert_databasesize)
            Databasesize_Result=self.mysqlconn.SelectData(select_databasesize_id)
            DatabasesizeId=Databasesize_Result
        return DatabasesizeId['data']

    def GetTableInfoId(self,InsertDatabase,InsertTableInfo,table_name,database_id,mysql_id,host_id):
        select_tableinfo_id = "select id from %s.%s where table_name='%s' and  table_mysql_id='%s' and table_database_id='%s';"  % (InsertDatabase,InsertTableInfo,table_name,mysql_id,database_id)
        insert_tableinfo = "insert into %s.%s(table_name,table_database_id,table_mysql_id,table_host_id) value('%s','%s','%s','%s');" % (InsertDatabase,InsertTableInfo,table_name,database_id,mysql_id,host_id)
        #print(insert_tableinfo)
        TableinfoId = self.mysqlconn.SelectData(select_tableinfo_id)
        if  int(TableinfoId['data']) == 0:
            self.mysqlconn.InsertData(insert_tableinfo)
            Tableinfo_Result = self.mysqlconn.SelectData(select_tableinfo_id)
            TableinfoId=Tableinfo_Result
        return  TableinfoId['data']


    def GetTableCountId(self,InsertDatabase,InsertTableCount,table_id,table_count):
        select_tablecount_id = "select id from %s.%s where table_info_id='%s' and create_date like '%s%s';" % (InsertDatabase,InsertTableCount,table_id,Yesterday,'%')
        insert_tablecount = "insert into %s.%s(table_count,create_date,update_date,table_info_id) value('%s','%s','%s','%s');" % (InsertDatabase,InsertTableCount,table_count,Yesterday,Today,table_id)
        TablecountId = self.mysqlconn.SelectData(select_tablecount_id)
        if  int(TablecountId['data'])==0:
            if int(table_count) != 0:
                self.mysqlconn.InsertData(insert_tablecount)
                Tablecount_Result = self.mysqlconn.SelectData(select_tablecount_id)
                TablecountId = Tablecount_Result
        return TablecountId['data']

    def GetTopId(self,InsertDatabase,InsertDatabaseSize):
        linuxoscommad=LinuxOSCommand()
        guandao = "| grep -v id | head -1 | awk '{print $1}'"
        select_one_size = "select id from %s.%s where create_date like '%s%s';"  % (InsertDatabase,InsertDatabaseSize,Yesterday,'%')
        command = "%s -e \"%s\" %s"  % (self.connect,select_one_size,guandao)
        result = linuxoscommad.LinuxOsCommand(command)
        return result[0]

    def GetTopSize(self,InsertDatabase,InsertDatabaseSize,Num,Date):
        TopSize={}
        linuxoscommad=LinuxOSCommand()
        result = self.GetTopId(InsertDatabase,InsertDatabaseSize)
        if result:
            SelectSQL="use %s;select ip,mysql_port,database_name,database_size,create_date from app01_hostinfo,app01_mysqlinfo,app01_databaseinfo,app01_databasesize  where app01_databasesize.database_info_id=app01_databaseinfo.id and app01_databaseinfo.database_mysql_id=app01_mysqlinfo.id  and  app01_mysqlinfo.mysql_host_id=app01_hostinfo.id and app01_databasesize.create_date like '%s%s' order by  database_size desc limit %s;" % (InsertDatabase,Date,'%',Num)
            CMD = "%s -e \"%s\""  % (self.connect,SelectSQL)
            cmd_result=linuxoscommad.LinuxOsCommand(CMD)
            tmp_list=[]
            for  i in list(range(len(cmd_result))):
                cmd_result_list = cmd_result[i].split('\t')
                tmp_list.append(tuple(cmd_result_list))  
            TopSize['data']=tuple(tmp_list)
#            print(TopSize)
            return TopSize
        else:
            print("%s当天数据不存在" % Date)

    def GetTopCount(self,InsertDatabase,InsertTableCount,Num,Date):
        TopCount={}
        linuxoscommad=LinuxOSCommand()
        result = self.GetTopId(InsertDatabase,InsertTableCount)
        if result:
            SelectSQL="use %s;select ip,mysql_port,database_name,table_name,table_count,create_date from app01_tablecount,app01_tableinfo,app01_hostinfo,app01_mysqlinfo,app01_databaseinfo  where app01_tablecount.table_info_id=app01_tableinfo.id and app01_tableinfo.table_host_id=app01_hostinfo.id  and  app01_tableinfo.table_mysql_id=app01_mysqlinfo.id  and app01_tableinfo.table_database_id=app01_databaseinfo.id and app01_tablecount.create_date like '%s%s' order by  table_count desc limit %s;"  % (InsertDatabase,Date,'%',Num)
            CMD = "%s -e \"%s\""  % (self.connect,SelectSQL)
            cmd_result=linuxoscommad.LinuxOsCommand(CMD)
            tmp_list=[]
            for  i in list(range(len(cmd_result))):
                cmd_result_list = cmd_result[i].split('\t')
                tmp_list.append(tuple(cmd_result_list))  
            TopCount['data']=tuple(tmp_list)
#            print(TopCount)
            return TopCount
        else:
             print("%s当天数据不存在" % Date)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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
    collect_datas=CollectMain()
    import_data_conn=LinuxMysqlImportData('192.168.30.191','3306','yxroot','srtadmin','/tmp/mariadb_3306.sock')
    for host_port,collect_data in collect_datas.items():
        print(collect_data)
        Host = import_data_conn.HandleHostData(collect_data)
        Port = import_data_conn.HandlePortData(collect_data) 
        Sizedata = import_data_conn.HandleSizeData(collect_data)
        Countdata = import_data_conn.HandleCountData(collect_data)
        host_id=import_data_conn.GetHostId(InsertDatabase,InsertHostInfo,Host)
        mysql_id=import_data_conn.GetMysqlId(InsertDatabase,InsertMysqlInfo,Port,host_id)
        #Insert Mysql Database Size
        for db_name,db_size in Sizedata.items():
            db_size = db_size.split('MB')[0]
            databaseinfo_id = import_data_conn.GetDatabaseInfoId(InsertDatabase,InsertDatabaseInfo,mysql_id,db_name)
            databasesize_id = import_data_conn.GetDatabaseSizeId(InsertDatabase,InsertDatabaseSize,databaseinfo_id,db_size)
            #print(host_id,mysql_id,databaseinfo_id,databasesize_id)
        for database_name,database_value in Countdata.items():
            for table_name,table_count in database_value.items():
                databasename_id = import_data_conn.GetDatabaseInfoId(InsertDatabase,InsertDatabaseInfo,mysql_id,database_name)
                table_id = import_data_conn.GetTableInfoId(InsertDatabase,InsertTableInfo,table_name,databasename_id,mysql_id,host_id)
                tablecount_id = import_data_conn.GetTableCountId(InsertDatabase,InsertTableCount,table_id,table_count)
                print(host_id,mysql_id,databasename_id,table_id,tablecount_id)
    print("--------------Ended----------------")

def AnalyMain():
    InsertDatabase='dbcount'
    InsertHostInfo='app01_hostinfo'
    InsertMysqlInfo='app01_mysqlinfo'
    InsertDatabaseInfo='app01_databaseinfo'
    InsertDatabaseSize='app01_databasesize'
    InsertTableInfo='app01_tableinfo'
    InsertTableCount='app01_tablecount'
    InsertMysqlInfos={1:{'host':'192.168.30.191','port':'3306','user':'root','password':'srtadmin','socket':'/tmp/mariadb_3306.sock'},
           }
    Len = len(sys.argv)
    if Len == 4:
        Num=sys.argv[2]
        Date = sys.argv[3]
    elif Len == 3:
        Num=sys.argv[2]
        Date = Yesterday
    else:
        Num = 100
        Date = Yesterday
    #print(sys.argv[1],sys.argv[2])
    import_data_conn=LinuxMysqlImportData('192.168.30.191','3306','yxroot','srtadmin','/tmp/mariadb_3306.sock')
    print("数据库信息分析<------------------Starting-------------------------->")
    print("%s数据库库最大的%s个库:" % (Yesterday,Num))
    data1 = import_data_conn.GetTopSize(InsertDatabase,InsertDatabaseSize,Num,Date)
    #print(data1['data'])
    print("%s数据库表总记录数最多的%s个表:" % (Yesterday,Num))
    data2 = import_data_conn.GetTopCount(InsertDatabase,InsertTableCount,Num,Date)
    #print(data2['data'])
    print("数据库信息分析<--------------------------End---------------------------->")
    SaveDir='/root/workspace/backup/mysql-analy'
    SaveDirFileName='mysql_analyse_%s_top%s.xls'   % (Yesterday,Num)
    #SaveDirFile = '%s/mysql_analyse_%s_top%s.xls' % (SaveDir,Yesterday,Num)
    SaveDirFile = '%s/%s' % (SaveDir,SaveDirFileName)
    LinuxWriteExcelTwo(data1['data'],data2['data'],'DatabaseSize','TableCount',SaveDirFile)
    print("详细信息见文件%s"  % SaveDirFile)
    '''
    [命令行]分析结果发送邮件
    print("---------------------------------------------------------------------------------")
    linuxoscomm=LinuxOSCommand()
    linuxoscomm.LinuxOsCommand('/usr/local/bin/python3 /root/workspace/scripts-python/linux_devops_plugins/base_py3/send_mail_py3.py')
    '''
    import global_setting
    from base_py3.send_mail_py3 import sendmailfile
    sendmailfile(Num,SaveDir,SaveDirFileName)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    Num = len(sys.argv)
    #Operation = input('\033[35;1m请输入需要执行的操作:\033[0m')
    if Num !=1:
       Operation=sys.argv[1]
       if Operation == 'collectmain':
               CollectMain()
       elif Operation == 'importmain':
               ImportMain()
       elif Operation == 'analymain':
               AnalyMain()
       else:
            print("python3 %s Argv:[collectmain/importmain/analymain]" % sys.argv[0])
    elif Num==1:
        AnalyMain()
    '''
    mysqlconn=LinuxMysqlCollectData('192.168.30.191','3306','yxroot','srtadmin','/tmp/mariadb_3306.sock') 
    print(mysqlconn.MysqlPing('ping'))
    '''
