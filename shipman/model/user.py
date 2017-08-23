#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Created on 2017-6-10 by Author:GuoLikai

""" 执行mysql语句 """
import hashlib

from shipman.settings import DATABASES
from shipman.model.mysql_server import MysqlServer

class UserSqlOperation(object):
    @staticmethod
    def check_adm_login(admname):
        db = MysqlServer(DATABASES)
        sql = "select `name`,`password`,`user_group` from user where name='%s'" % admname
        ret = db.run_sql(sql)
        db.close()
        return ret

    def insert_user_data(name,password,user_group):
        db = MysqlServer(DATABASES)
        sql = "insert into user(name,password,user_group) values(%s','md5(%s)','%s')" % (name,password,user_group)
        db.execute_sql(sql)
        db.close()
        return 0

if __name__ == '__main__':
    usermsg = {'name':'admin','password':'123456', 'user_group':'Admin'}
    name, password, user_group = usermsg['name'],usermsg['password'],usermsg['user_group']
    userinfo = UserSqlOperation()
    ret = userinfo.insert_user_data(name, password, user_group)
    #insert into user(name,password,user_group) values('admin',md5(123456),'Admin')
    if ret ==0:
        print(u'%s用户插入成功' % name)
