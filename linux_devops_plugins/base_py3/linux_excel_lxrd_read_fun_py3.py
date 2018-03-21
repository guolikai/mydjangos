#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#Author:GuoLikai@2018-03-21 16:14:30

import xlrd

def readinfo(xlsfile):
	# 读取表格中的基本信息
	#xlsfile = r"/root/cdn/deyang.xlsx"           				# 打开指定路径中的xls文件
	book = xlrd.open_workbook(xlsfile)             				# 得到Excel文件的book对象，实例化对象
	sheet0 = book.sheet_by_index(0)                 			# 通过sheet索引获得sheet对象
	#print("通过sheet索引获得sheet对象:",sheet0)
	sheet_name =book.sheet_names()[0]              				# 获得指定索引的sheet表名字
	print ("获得指定索引的sheet表名字:",sheet_name)
	sheet1 =book.sheet_by_name(sheet_name)         				# 通过sheet名字来获取，当然如果知道sheet名字就可以直接指定
	nrows = sheet0.nrows                           				# 获取行总数
	print ("获取%s行总数:%s" % (sheet_name,nrows))
	ncols = sheet0.ncols                             			# 获取列总数
	print ("获取列总数:",ncols)

def ReadAllData(xlsfile,index):
	# 读取表格中的所有数据
	#xlsfile = r"/root/cdn/deyang.xlsx"            				# 打开指定路径中的xls文件
	book = xlrd.open_workbook(xlsfile)             				# 得到Excel文件的book对象，实例化对象
	#sheet_index = book.sheet_by_index(index)                 	# 通过sheet索引获得sheet对象
	#print("通过sheet索引获得sheet对象:",sheet0)
	sheet_name = book.sheet_names()[index]              		# 获得指定索引的sheet表名字
	print ("获得指定索引的sheet表名字:",sheet_name)
	sheet_index =book.sheet_by_name(sheet_name)         		# 通过sheet名字来获取，当然如果知道sheet名字就可以直接指定
	nrows = sheet_index.nrows                           		# 获取行总数
	ncols = sheet_index.ncols                          			# 获取列总数
	print ("获取%s行总数:%s" % (sheet_name,nrows))
	print ("获取%s列总数:%s" % (sheet_name,ncols))

	#循环打印每一行每一列的内容
	res = {}
	for line in range(nrows):									#循环打印每一行的内容
		col_list = []											#以列表形式循环获取每一列的内容
		for col in range(ncols):
			col_list.append(sheet_index.row_values(line)[col])
		#print(col_list)
		res[line] = tuple(col_list)								#列表装换为元祖
	return res
	#对获取到的数据字典进行第二列的取值
	#for key,value in res.items():
	#	print(value[1])

def ReadLineData(xlsfile,index,row):
	# 通过行数读取表格中的数据
	#xlsfile = r"/root/cdn/deyang.xlsx"            				# 打开指定路径中的xls文件
	book = xlrd.open_workbook(xlsfile)             				# 得到Excel文件的book对象，实例化对象
	sheet_index = book.sheet_by_index(index)       				# 通过sheet索引获得sheet对象
	#ncols = sheet_inde.ncols                      				# 获取列总数
	#print ("获取列总数:",ncols)
	row_data = sheet_index.row_values(row)         				# 获得第row行的数据列表
	return row_data

def ReadColumnData(xlsfile,index,col):
	# 通过列数读取表格中的数据
	#xlsfile = r"/root/cdn/deyang.xlsx"            				# 打开指定路径中的xls文件
	book = xlrd.open_workbook(xlsfile)             				# 得到Excel文件的book对象，实例化对象
	sheet_index = book.sheet_by_index(index)       				# 通过sheet索引获得sheet对象
	#ncols = sheet_inde.ncols                      				# 获取列总数
	#print ("获取列总数:",ncols)
	col_data = sheet_index.col_values(col)        				 # 获得第col列的数据列表
	return col_data

def ReadCellData(xlsfile,index,row,col):
	# 通过坐标读取表格中的数据
	#xlsfile = r"/root/cdn/deyang.xlsx"            				# 打开指定路径中的xls文件
	book = xlrd.open_workbook(xlsfile)             				# 得到Excel文件的book对象，实例化对象
	sheet_index = book.sheet_by_index(index)        			# 通过sheet索引获得sheet对象
	cell_value = sheet_index.cell_value(row,col)
	print ("获取【%s】表中第%s张第%s行第%s列的数据:%s" % (xlsfile,index+1,row+1,col+1,cell_value))
	return cell_value

if __name__ == '__main__':
	xlsfile = r"D:/deyang.xlsx"          			# 打开指定路径中的xls文件
	readinfo(xlsfile)
	#print(ReadAllData(xlsfile,0))
	#print(ReadLineData(xlsfile,0,0))
	print(ReadColumnData(xlsfile,0,0))
	#print(ReadCellData(xlsfile,0,0,1))