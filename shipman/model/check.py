#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Created on 2017-6-10 by Author:GuoLikai

#from .node import NodeInfo
#与数据库相关的user操作
from shipman.model.user import UserSqlOperation
from shipman.model.node import NodeInfo
from shipman.handler.base import BaseHandler


class Check(BaseHandler):
    @staticmethod
    def md5(result):
        import hashlib
        m = hashlib.md5()
        m.update(result.encode('utf-8'))   #浏览器传入的数据是gdk，在此做下转换；
        return m.hexdigest()


    @staticmethod
    def login_check(input_username, input_password):
        mysql_adm_password = UserSqlOperation.check_adm_login(input_username)
        #print(mysql_adm_password)
        if mysql_adm_password:
            md5_input_password = Check.md5(input_password)
            if mysql_adm_password[0][1] == md5_input_password:
                return mysql_adm_password[0][2]
            else:
                return "Incorrect password"
        else:
            return "Invalid username"

    @staticmethod
    def node_check(result, check):
        if check:
            node_ret = NodeInfo.get_node_modify(result['ip'])
            if not node_ret:
                return 0
        else:
            return

    @staticmethod
    def ip_check(result, check):
        if check:
            ip_ret = NodeInfo.get_ip_modify(result['ip_addr'])
            print(ip_ret)
            if not ip_ret:
                return 0
        else:
            return