#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#Author:GuoLikai@2017-11-27 14:30:10

import xlwt

def LinuxWriteExcelArray(Data,TableName,SaveDirFile):
    workbook=xlwt.Workbook(encoding='utf-8')  
    booksheet=workbook.add_sheet(TableName,cell_overwrite_ok=True)
    for i,row in enumerate(Data):  
        for j,col in enumerate(row):
            booksheet.write(i,j,col)  
    workbook.save('%s' % (SaveDirFile))

def LinuxWriteTwo(Data1,Data2,Table1,Table2,SaveDirFile):
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

def GetDictValue(data,item):
    for i,k in data.items(): 
        if i==item:
            return data[i]


def main():
    data = (('ip','mysql_port','database_name','table_name','table_count','create_date'),
            ('10.10.20.220','3307','nova','instance_system_metadata','3221','2017-11-26'),
            ('10.10.20.220','3306','nova','instance_system_metadata','3005','2017-11-26'),
            ('192.168.30.191','3307','nova','instance_system_metadata','3221','2017-11-26'),
            ('192.168.30.191','3306','nova','instance_system_metadata','3005','2017-11-26'),
            )
    #LinuxWriteExcelArray(data,'Database Size','/root/analy_log.xls')
#--------------------------------------------------------------------------------------------------------------------------------------------
    Data={'192.168.30.191_3306':{'ip':'192.168.30.191','mysql_port':'3306','database_name':'nova','table_name':'instance','table_count':'3333','create_date':'2017-11-26'},
          '192.168.30.191_3307':{'ip':'192.168.30.191','mysql_port':'3307','database_name':'nova','table_name':'instance','table_count':'2222','create_date':'2017-11-25'},
        }

    Arrey=[('ip','mysql_port','database_name','table_name','table_count','create_date')]
    for key,value in Data.items():
        List=[]
        ip = GetDictValue(value,'ip')
        mysql_port = GetDictValue(value,'mysql_port')
        database_name = GetDictValue(value,'database_name')
        table_name = GetDictValue(value,'table_name')
        table_count = GetDictValue(value,'table_count')
        create_date = GetDictValue(value,'create_date')
        List.append(ip)
        List.append(mysql_port)
        List.append(database_name)
        List.append(table_name)
        List.append(table_count)
        List.append(create_date)
        List= tuple(List)
        Arrey.append(List)
    DATA=tuple(Arrey)
    #print(DATA)
    #LinuxWriteExcelArray(DATA,'Table Count','/root/analy_log.xls')
    #LinuxWriteTwo(data,DATA,'DatabaseSize','TableCount','/root/analy_log.xls')
    LinuxWriteTwo(data,DATA,'DatabaseSize','TableCount','/analy_log.xls')

if __name__ == '__main__':
    main()

