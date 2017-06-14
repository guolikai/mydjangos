#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Created on 2017-6-10 by Author:GuoLikai

from shipman.settings import DATABASES
from shipman.model.mysql_server import MysqlServer

class NodeInfo(object):
    @staticmethod
    def node_info():
        db = MysqlServer(DATABASES)
        sql = "select * from node"
        ret = db.run_sql(sql)
        db.close()
        return ret

    def get_node_info(node_ip):
        db = MysqlServer(DATABASES)
        sql = "select * from node where node_ip='%s'" % node_ip
        ret = db.run_sql(sql)
        db.close()
        return ret

    @staticmethod
    def get_node_name_group(node_ip,port):
        db = MysqlServer(DATABASES)
        sql = "select name,node_group from node where node_ip='%s' and port='%s'" % (node_ip,port)
        ret = db.run_sql(sql)
        db.close()
        return ret

    @staticmethod
    def group_list():
        db = MysqlServer(DATABASES)
        sql = "select distinct `node_group` from node"
        ret = db.run_sql(sql)
        db.close()
        return ret

    @staticmethod
    def node_list(node_group):
        db = MysqlServer(DATABASES)
        sql = "select  `node_ip` from node where node_group=" + '"' + node_group + '"'
        ret = db.run_sql(sql)
        db.close()
        return ret

    @staticmethod
    def get_node_port(node_ip):
        db = MysqlServer(DATABASES)
        sql = "select `port` from node where node_ip='%s'" % node_ip
        ret = db.run_sql(sql)
        db.close()
        return ret

    @staticmethod
    def get_node_ip(node_group):
        db = MysqlServer(DATABASES)
        sql = "select distinct `node_ip` from node where node_group='%s'" % node_group
        ret = db.run_sql(sql)
        db.close()
        return ret

    @staticmethod
    def delete_node_info(node_ip):
        db = MysqlServer(DATABASES)
        sql = "delete from node where node_ip='%s'" % node_ip
        db.execute_sql(sql)
        db.close()
        return 0


    @staticmethod
    def insert_node_usage(name,node_ip,port, node_group):
        db = MysqlServer(DATABASES)
        sql = "insert into node(name,node_ip,port,node_group) values('%s','%s','%s','%s')" % (name,node_ip,port, node_group)
        db.execute_sql(sql)
        db.close()
        return 0

    @staticmethod
    def update_node_info(node_info, state,node_ip):
        db = MysqlServer(DATABASES)
        #sql = "update node set name='%s',cpus='%s',mem='%s',images='%s',state='%s',containers='%s',os_version='%s',kernel_version='%s',docker_version='%s' where node_ip='%s'" % (node_info["Name"],node_info["NCPU"],node_info["MemTotal"],node_info["Images"],state,node_info["Containers"],node_info["OperatingSystem"],node_info["KernelVersion"],node_info["PkgVersion"],node_ip)
        sql = "update node set cpus='%s',mem='%s',images='%s',state='%s',containers='%s',os_version='%s',kernel_version='%s',docker_version='%s' where node_ip='%s'" % (node_info["NCPU"],node_info["MemTotal"],node_info["Images"],state,node_info["Containers"],node_info["OperatingSystem"],node_info["KernelVersion"],node_info["PkgVersion"],node_ip)
        ret = db.run_sql(sql)
        db.close()
        return ret

    @staticmethod
    def update_node_state(state,node_ip, port):
        db = MysqlServer(DATABASES)
        sql = "update node  set state='%s' where node_ip='%s' and port='%s'" % (state, node_ip,port)
        db.execute_sql(sql)
        db.close()
        return 0

    @staticmethod
    def update_node_name_group(name,node_group,node_ip,port):
        db = MysqlServer(DATABASES)
        sql = "update node set name='%s',node_group='%s' where node_ip='%s' and port='%s'" % (name,node_group,node_ip,port)
        ret = db.run_sql(sql)
        db.close()

    @staticmethod
    def update_node_name(name,node_ip,port,node_group):
        db = MysqlServer(DATABASES)
        sql = "update node set name='%s' where node_ip='%s' and port='%s' and node_group='%'" % (name,node_ip,port,node_group)
        ret = db.run_sql(sql)
        db.close()


#class ConUsage(object):
    @staticmethod
    def con_usage_info():
        db = MysqlServer(DATABASES)
        sql = "select `con_id`,`con_ip`,`con_name`,`node_ip`,`user_name`,`con_app`,`con_desc` from con_usage"
        result = db.run_sql(sql)
        db.close()
        return result

    @staticmethod
    def get_con_usage_modify(con_id):
        db = MysqlServer(DATABASES)
        sql = "select `con_id`,`con_ip`,`con_name`,`node_ip`,`user_name`,`con_app`,`con_desc` from con_usage where con_id='%s'" %  con_id
        ret = db.run_sql(sql)
        db.close()
        return ret

    @staticmethod
    def get_con_usage_info(con_id,node_ip):
        db = MysqlServer(DATABASES)
        sql = "select * from con_usage where con_id='%s' and node_ip='%s'" % (con_id,node_ip)
        ret = db.run_sql(sql)
        db.close()
        return ret


    @staticmethod
    def set_con_usage_modify(con_dic):
        db = MysqlServer(DATABASES)
        sql = "update con_usage set user_name='%s',con_app='%s',con_desc='%s' where con_id='%s'" % (con_dic['user_name'],
                                                                                  con_dic['con_app'],
                                                                                  con_dic['con_desc'],
                                                                                  con_dic['con_id'],)
        db.execute_sql(sql)
        db.close()
        return 0

    @staticmethod
    def get_con_usage_info(con_id,node_ip):
        db = MysqlServer(DATABASES)
        sql = "select * from con_usage where con_id='%s'and node_ip='%s'" % (con_id,node_ip)
        ret = db.run_sql(sql)
        db.close()
        return ret

    @staticmethod
    def insert_con_usage(con_id, con_ip,con_name,node_ip):
        db = MysqlServer(DATABASES)
        sql = "insert into con_usage(con_id,con_ip,con_name,node_ip) values('%s','%s','%s','%s')" % (con_id, con_ip,con_name,node_ip)
        db.execute_sql(sql)
        db.close()
        return 0

    @staticmethod
    def delete_con_usage(con_id):
        db = MysqlServer(DATABASES)
        sql = "delete from con_usage where con_id='%s'" % con_id
        db.execute_sql(sql)
        db.close()
        return 0

    @staticmethod
    def delete_con_usage_info(node_ip):
        db = MysqlServer(DATABASES)
        sql = "delete from con_usage where node_ip='%s'" % node_ip
        db.execute_sql(sql)
        db.close()
        return 0

    @staticmethod
    def get_con_usage_node_ip(con_id):
        db = MysqlServer(DATABASES)
        sql = "select node_ip from con_usage where con_id='%s'" % con_id
        ret = db.run_sql(sql)
        db.close()
        return ret

if __name__ == '__main__':
    nodeinfo = NodeInfo()
    result1 = nodeinfo.get_node_name_group('172.16.1.101','2375')
    print(result1[0])

