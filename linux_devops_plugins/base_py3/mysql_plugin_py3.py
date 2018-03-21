#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#Author:GuoLikai@2018-03-11 14:28:58


import sys
import os
import pymysql
#pymysql.install_as_MySQLdb()

import datetime
import time
import json

def get_data( sql,database ):
#	conn_in=MySQLdb.connect(host="192.168.30.191",user="root",passwd="srtroot",db=database,charset="utf8")
	conn_in=pymysql.connect(host="192.168.30.191",port=3306,user="yxroot",passwd="srtadmin",db=database,charset="utf8")
	#cursor_in = conn_in.cursor()     #查询数据返回的是字典
	cursor_in = conn_in.cursor(pymysql.cursors.DictCursor)
	cursor_in.execute(sql)
	rows    =   cursor_in.fetchall()
	cursor_in.close()
	conn_in.close()
	return rows
  
def exec_sql(sql, database):
	conn_in=MySQLdb.connect(host="192.168.30.191",user="root",passwd="srtroot",db=database,charset="utf8")
	cursor_in = conn_in.cursor()
	cursor_in.execute( sql)
	conn_in.commit()
	cursor_in.close()
	conn_in.close()
  
def get_yesterday( today, days):
	oneday = datetime.timedelta(days) 
	yesterday = today - oneday
	return yesterday

def main():
	today = datetime.date.today()
	yesterday=get_yesterday(today,-1)
	print(today,yesterday)
	sql = 'select host,user,password from mysql.user'
	result = get_data(sql,'mysql')
	print(len(result),type(result			))
	#for i in range(len(result)):
	#	print(result[i]['host'])
	#	print(result[i])
	for index,value in enumerate(result):
		print(index,value['host'])

if __name__ == '__main__':
	main()
