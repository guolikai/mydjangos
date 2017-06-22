#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Created on 2017-6-10 by Author:GuoLikai

import tornado.web
import threading
import sys
import json
import uuid
import time

from shipman.handler.base import BaseHandler
from shipman.myswarm import Myswarm
from shipman.settings import template_variables
from shipman.model.data_manage import DataManage
from shipman.model.node import NodeInfo
from shipman.config import basejson

class Main(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('node/main.html',)

class NodeManage(BaseHandler):
    @tornado.web.authenticated
    def get(self,*args, **kwargs):
        threads = []
        node_update = threading.Thread(target=self._update_node)
        threads.append(node_update)
        node_pass = threading.Thread(target=self._get_pass)   #此函数在于构成for循环，用于异构
        threads.append(node_pass)
        for t in threads:
            t.setDaemon(True)
            t.start()
        node_data = NodeInfo.node_info()
        node_data_handled = DataManage.manage_node_info(node_data) #对数据按页面要求的格式做格式化
        self.render("node/node_manage.html", node_data = node_data_handled)

    def _update_node(self):
        node_data = NodeInfo.node_info()   #获取Node节点信息
        myswarm = Myswarm()
        for line in node_data:
            node_ip = line[2]
            node_port = line[3]
            if myswarm.ping_port(node_ip, node_port) == 0:
                node_info = myswarm.node_info(node_ip, node_port)
                NodeInfo.update_node_info(node_info,myswarm.ping_port(node_ip, node_port),node_ip)
            else:
                NodeInfo.update_node_state(myswarm.ping_port(node_ip, node_port),node_ip,node_port)
                continue

    def _get_pass(self):
        pass

class Top(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("base.html", name = template_variables)

class LeftGroup(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('node/leftgroup.html')

class GroupList(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        id = self.get_argument("id", None)
        lv = self.get_argument("lv", None)
        name = self.get_argument("n", None)
        alldata = []
        if id == None and lv == None and name == None:
            alldata = self._getgroup()
        elif id != "" and lv == "0":
            alldata = self._getnode(id, name)
        elif lv == "1":
            alldata = self._getcontainer(id, name)
        self.write(json.dumps(alldata))

    def _getgroup(self):
        group_data = []
        group_ret  = NodeInfo.group_list()
        for i in DataManage.group_list(group_ret):
            group_data.append(i)
        #print(group_data)
        return group_data


    def _getnode(self, id, name):
        node_ret  = NodeInfo.node_list(name)
        node_data = DataManage.node_list(node_ret, id, name)
        return node_data

    def _getcontainer(self, id, name):
        container_ret  = NodeInfo.container_list(name)
        container_data = DataManage.container_list(container_ret, id, name)
        return container_data

class NodeAdd(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwarg):
        self.render("node/node_add.html")

    def post(self, *args, **kwargs):
        con_dict = {}
        for key in ['name','node_ip', 'port', 'node_group']:
            con_dict[key] = self.get_argument(key)
        node_ip = con_dict["node_ip"]
        port = con_dict["port"]
        node_group = con_dict["node_group"]
        name = con_dict["name"]
        myswarm = Myswarm()
        if myswarm.ping_port(node_ip,port) == 0:
            if len(name) == 0:
                node_info = myswarm.node_info(node_ip, port)
                name = node_info["Name"]
            get_node_ret = NodeInfo.get_node_name_group(node_ip,port)
            #print(get_node_ret)
            if len(get_node_ret) == 0:
                NodeInfo.insert_node_usage(name,node_ip,port,node_group)
                self.write(u"Node [Ip:%s port:%s]  add successfully" % (node_ip,port))
            elif get_node_ret[0][0] == node_group:
                self.write("There is already exists node[Ip:%s port:%s group:%s] of the node" % (node_ip,port,node_group))
            else:
                NodeInfo.update_node_name_group(name,node_group,node_ip,port)
        else:
            self.write(u"Node [Ip:%s port:%s] Docker has not Running" % (node_ip,port))

class NodeModify(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwarg):
        node_ip = self.get_argument('node_ip')
        node_data = NodeInfo.get_node_info(node_ip)
        node_data_handled = DataManage.manage_node_info(node_data)
        self.render("node/node_modify.html", name=template_variables, single_con_usage_data = node_data_handled)

    def post(self, *args, **kwargs):
        con_dict = {}
        for key in ['name','node_ip', 'port', 'node_group']:
            con_dict[key] = self.get_argument(key)

        name = con_dict["name"]
        node_ip = con_dict["node_ip"]
        port = con_dict["port"]
        node_group = con_dict["node_group"]
        myswarm = Myswarm()

        if myswarm.ping_port(node_ip,port) == 0:
            if len(name) == 0:
                node_info = myswarm.node_info(node_ip, port)
                name = node_info["Name"]
            if len(node_group) == 0:
                group_msg = NodeInfo.get_node_name_group(node_ip, port)
                node_group = group_msg[0][1]
            get_node_ret = NodeInfo.get_node_name_group(node_ip,port)
            if len(get_node_ret) == 0:
                NodeInfo.insert_node_usage(name,node_ip,port,node_group)
                self.write(u"Node [Ip:%s port:%s] add successfully" % (node_ip,port))
            else:
                NodeInfo.update_node_name_group(name,node_group,node_ip,port)
                self.write(u"Node modify successfully")
        else:
            self.write(u"Node [Ip:%s port:%s] Docker has not Running" % (node_ip,port))

class NodeDelete(BaseHandler):
        @tornado.web.authenticated
        def get(self, *args, **kwarg):
            pass
        def post(self):
            ret = {}
            node_ip = self.get_argument("node_ip")
            delete_node_ret =  NodeInfo.delete_node_info(node_ip)
            if delete_node_ret == 0:
                delete_con_ret =  NodeInfo.delete_con_usage_info(node_ip)
                if delete_con_ret == 0:
                    self.write("Node %s delete ok" % node_ip)
                    ret['message'] = "Node %s delete ok" % node_ip
                    ret['status'] = 0
            else:
                #self.write("Node %s delete happend something roung" % node_ip)
                ret['message'] = "Node %s delete happend something roung" % node_ip
                ret['status'] = 1
            ret = json.dumps(ret)
            self.write(ret)

class RightNode(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        node_ip = self.get_argument('node_ip', None)
        #print(node_ip)
        if node_ip is None:
            self.write("Something Wrong")
            return
        else:
            node_port = NodeInfo.get_node_port(node_ip)[0][0]
            myswarm = Myswarm()
            con_data = myswarm.container_list(node_ip,node_port)
            #print("con_data",con_data)
            for con in con_data:
                #print(con_data[con]["id_num"],con_data[con]["con_ip"],node_ip)
                ret = NodeInfo.get_con_usage_info(con_data[con]["id_num"],node_ip)
                if len(ret) == 0:
                    NodeInfo.insert_con_usage(con_data[con]["id_num"],con_data[con]["con_ip"],con_data[con]["con_name"],node_ip)
                else:
                    continue
            self.render('node/rightnode.html', con_data = con_data, node_ip = node_ip)

class ConCreate(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        node_ip = self.get_argument('node_ip', None)
        if node_ip is None:
            self.write("Something Wrong")
            return
        else:
            node_port = NodeInfo.get_node_port(node_ip)[0][0]
            myswarm = Myswarm()
            images_data = myswarm.images_list(node_ip, node_port)
            self.render('node/con_create.html', node_ip = node_ip, images = images_data)

    def post(self, *args, **kwargs):
        json_ret = json.loads(basejson[0])
        node_ip = self.get_argument('node_ip', 'None')
        if node_ip == 'None':
            print("There is no node ip")
            return

        port_ret = NodeInfo.get_node_port(node_ip)
        if len(port_ret) < 1:
            print("There is no port of the node")
            return
        else:
            node_port = port_ret[0][0]

        con_name = self.get_argument('con_name',None)
        con_num = self.get_argument('con_num', None)
        if len(con_num) == 0:
            con_num = 1
        con_num = int(con_num)
        print(u'待创建容器个数:%s'% (con_num))

        con_dict = {}
        for key in ['Cmd', 'Image', 'CpuPeriod', 'CpuQuota', 'CpuShares', 'Memory']:
            con_dict[key] = self.get_argument(key.lower())
            if key == 'Cmd' and con_dict[key] != "":
                json_ret[key] = con_dict[key].split()
            elif key == 'Image' and con_dict[key] != "":
                json_ret[key] = con_dict[key]
            elif con_dict[key] != "":
                json_ret['HostConfig'][key] = int(con_dict[key])

        name_list = []
        if con_num > 1:
            for num in range(con_num):
                #print(num + 1)
                if len(con_name) == 0:
                    con_name = str(uuid.uuid4())[0:13]
                    #print(u'待创建容器名:%s' % con_name)
                    name_list.append(con_name)
                    con_name = ''
                else:
                    con_name = '%s%s' % (con_name, str(num + 1))
                    #print(u'待创建容器名:%s' % con_name)
                    name_list.append(con_name)
                    con_name = con_name[:-len(str(num + 1))]
        else:
            if len(con_name) == 0:
                con_name = str(uuid.uuid4())[0:13]
            name_list.append(con_name)

        threads = []
        create_con = threading.Thread(target=self._create_con,args=(name_list,node_ip,node_port,json_ret))
        threads.append(create_con)
        create_pass = threading.Thread(target=self._create_pass)   #此函数在于构成for循环，用于异构
        threads.append(create_pass)
        #print(threads)
        for t in threads:
            t.setDaemon(True)
            t.start()
        t.join()
        #time.sleep(con_num*2)
        time.sleep(1)
        self.write(u"%s节点上容器创建并启动成功" % (node_ip))


    def _create_con(self,name_list,node_ip, node_port, json_ret):
        #print(name_list)
        for i in range(len(name_list)):
            #time.sleep(0.1)
            if len(name_list[i]) == 0:
                json_ret['Name'] = str(uuid.uuid4())[0:13]
                json_ret['Hostname'] = json_ret['Name']
            elif len(name_list[i]) == 13:
                json_ret['Name'] = name_list[i]
                json_ret['Hostname'] = name_list[i]
            else:
                json_ret['Name'] = name_list[i]
                json_ret['Hostname'] = str(uuid.uuid4())[0:13]
            print(u'节点:[%s],端口:[%s],容器ID:[%s],容器名:[%s]' % (node_ip, node_port, json_ret['Hostname'], json_ret['Name']))
            myswarm = Myswarm()
            if NodeInfo.get_con_usage_info(json_ret['Hostname'],node_ip):
                continue
            elif NodeInfo.get_con_usage_con_name(node_ip,json_ret['Name']):
                continue
            else:
                container_id = myswarm.create_container(node_ip, node_port, json_ret)
                if not container_id:
                    print("Can not create the Container")
                    return
                #print(node_ip, node_port,container_id)
                ret = myswarm.start_container(node_ip, node_port, container_id)
                print(u"%s节点上容器%s创建并启动成功" % (node_ip,container_id[0:12]))

    def _create_pass(self):
        pass

class ConAction(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        #node_ip = self.get_argument('node_ip')
        con_id  = self.get_argument('con_id')
        con_node_ip = NodeInfo.get_con_usage_node_ip(con_id)
        #print(node_ip,con_node_ip[0][0])
        #if node_ip != con_node_ip[0][0]:
        #   node_ip = con_node_ip[0][0]
        node_ip = con_node_ip[0][0]
        port_ret = NodeInfo.get_node_port(node_ip)
        if len(port_ret) < 1:
            print("There is no port of the node")
            return
        else:
            node_port = port_ret[0][0]

        myswarm = Myswarm()
        con_data_handled = myswarm.container_info(node_ip, node_port, con_id)
        self.render("node/con_action.html", name=template_variables, node_ip=node_ip,
            node_port=node_port, con_id=con_id, con_data=con_data_handled)

class ConStart(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kargs):
        con_dict = {}
        for key in ['node_ip', 'port', 'con_id']:
            con_dict[key] = self.get_argument(key)
        myswarm = Myswarm()
        if not con_dict['con_id']:
            self.write("There is no container id")
        print("Starting the container......")
        ret = myswarm.start_container(con_dict['node_ip'], con_dict['port'], con_dict['con_id'])
        self.write(u"%s节点上容器%s已启动" % (con_dict['node_ip'],con_dict['con_id']))

class ConStop(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kargs):
        con_dict = {}
        for key in ['node_ip', 'port', 'con_id']:
            con_dict[key] = self.get_argument(key)
        myswarm = Myswarm()
        myswarm.stop_container(con_dict['node_ip'], con_dict['port'], con_dict['con_id'])
        self.write(u"%s节点上容器%s已停止" % (con_dict['node_ip'],con_dict['con_id']))

class ConRestart(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kargs):
        con_dict = {}
        for key in ['node_ip', 'port', 'con_id']:
            con_dict[key] = self.get_argument(key)

        container_ip = {}
        myswarm = Myswarm()
        if not con_dict['con_id']:
            self.write("There is no container id")
        myswarm.stop_container(con_dict['node_ip'], con_dict['port'], con_dict['con_id'])
        time.sleep(2)
        myswarm.start_container(con_dict['node_ip'], con_dict['port'], con_dict['con_id'])
        self.write(u"%s节点上容器%s已重启" % (con_dict['node_ip'],con_dict['con_id']))

class ConDestroy(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kargs):
        con_dict = {}
        for key in ['node_ip', 'port', 'con_id']:
            con_dict[key] = self.get_argument(key)
        myswarm = Myswarm()
        myswarm.destroy_container(con_dict['node_ip'], con_dict['port'], con_dict['con_id'])
        self.write(u"%s节点上容器%s销毁" % (con_dict['node_ip'],con_dict['con_id']))

class ConManage(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        con_id = self.get_argument('con_id', 'none')
        if con_id == 'none':
            con_data = NodeInfo.con_usage_info()
        else:
            con_data = NodeInfo.get_con_usage_modify(con_id)
        con_data_handled = DataManage.manage_con_usage_info(con_data)
        self.render("node/con_list.html", name=template_variables, con_data=con_data_handled)

class ConModify(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        con_id = self.get_argument('con_id')
        con_data = NodeInfo.get_con_usage_modify(con_id)
        con_data_handled = DataManage.manage_con_usage_info(con_data)
        self.render("node/con_modify.html", name=template_variables, single_con_usage_data = con_data_handled)

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        con_dic = dict()
        for key in ['con_id', 'con_desc', 'con_app', 'user_name']:
            con_dic[key] = self.get_argument(key)
        con_ret = NodeInfo.set_con_usage_modify(con_dic)
        if con_ret == 0:
            url_cmd = ("<script language='javascript'>window.location.href='" +
                        "/conmanage?con_id=" + str(con_dic['con_id']) + "';</script>")
            self.write(url_cmd)
        else:
            self.write("<script language='javascript'>alert('修改失败');window.location.href='/conmanage';</script>")

class Group(BaseHandler):
    def get(self, *args, **kwargs):
        group_name = self.get_argument('group_name',None)
        #print(group_name)
        data_list = {}
        self.num = 1
        node_ip_list = NodeInfo.get_node_ip(group_name)
        #print(node_ip_list,len(node_ip_list))
        for index in range(len(node_ip_list)):
            node_ip = node_ip_list[index][0]
            #print('---',node_ip)
            if node_ip is None:
                self.write("Something Wrong")
                return
            else:
                node_port = NodeInfo.get_node_port(node_ip)[0][0]
                myswarm = Myswarm()
                con_data = myswarm.container_list(node_ip, node_port)
                for con in con_data:
                    #print(con_data[con])
                    data_list[self.num] = con_data[con]
                    self.num += 1
        #print(data_list)
        self.render('node/groupconlist.html', con_data=data_list,node_ip=node_ip,group_name=group_name)


if __name__ == '__main__':
    nodemodify = NodeModify()
    nodemodify.delete('')