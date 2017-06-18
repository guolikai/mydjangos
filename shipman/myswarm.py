#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Created on 2017-6-10 by Author:GuoLikai

import docker
import socket
import time

from shipman.curl import Curl
from shipman.model.node import NodeInfo

class Myswarm(object):
    def ping_port(self, ip, port):
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cs.settimeout(0.2)
        address = (str(ip), int(port))
        try:
            cs.connect((address))
        except socket.error as e:
            print(e)
            return 1
        cs.close()
        return 0

    def delete_con_usage(self, container_id):
        if not container_id:
            return
        else:
            NodeInfo.delete_con_usage(container_id)

    def _container_detail(self, node_ip, node_port, containers_id):
        url = ('http://' + node_ip + ":" + node_port + "/containers/" + containers_id + "/json")
        container_more_url = Curl(url)
        ret_json = container_more_url.get_value()
        return ret_json

    def container_list(self, node_ip, node_port):
        #print(node_ip)
        #print(node_port)
        url = 'http://' + node_ip + ":" + node_port + "/containers/json?all=1"
        container_url = Curl(url)
        ret_json = container_url.get_value()

        con_data = {}
        container_id = []
        if ret_json:
            for i in ret_json:
                container_id.append(i['Id'][0:12])
        else:
            return con_data

        if len(container_id) < 1:
            return con_data
        else:
            con_data = {}
            con_num = 1
            for con_id in container_id:
                tmp_dict = {}
                ret_json = self._container_detail(node_ip, node_port, con_id)
                if len(ret_json) < 1:
                    return con_data
                con_state = ""
                if ('Running' in ret_json['State'].keys()) and (
                    'Status' not in ret_json['State'].keys()):  # for docker 1.7
                    con_state = str(ret_json['State']['Running'])
                elif 'Status' in ret_json['State'].keys():  # for docker 1.9 and higher
                    con_state = str(ret_json['State']['Status'])
                else:  # for else
                    con_state = "Exited"
                tmp_dict['id_num'] = ret_json['Id'][0:12]
                tmp_dict['con_ip'] = ret_json['NetworkSettings']['IPAddress']
                tmp_dict['con_name'] = ret_json['Name'].replace('/','')
                tmp_dict['cpuperiod'] = ret_json['HostConfig']['CpuPeriod']
                tmp_dict['cpuquota'] = ret_json['HostConfig']['CpuQuota']
                tmp_dict['memory'] = ret_json['HostConfig']['Memory']
                tmp_dict['state'] = con_state
                tmp_dict['cmd'] = str(ret_json['Config']['Cmd'])
                tmp_dict['created'] = ret_json['State']['StartedAt']
                con_data[con_num] = tmp_dict
                con_num += 1
        return con_data

    def images_list(self, node_ip, node_port):
        client_ins = docker.Client(base_url='tcp://' + node_ip + ':' + node_port, version='1.20', timeout=5)
        ret_json = client_ins.images()
        images_list = []
        for one in ret_json:
            images_list.append(one['RepoTags'])
        return images_list

    def create_container(self, node_ip, node_port, conf):
        client_ins = docker.Client(base_url='tcp://' + node_ip + ":" + node_port, version='1.20', timeout=5)
        print("      Create the container......")
        container_ret = client_ins.create_container(image=conf['Image'],
                                                    stdin_open=conf['OpenStdin'],
                                                    tty=conf['Tty'],
                                                    command=conf['Cmd'],
                                                    name=conf['Name'],
                                                    hostname=conf['Hostname'],
                                                    host_config=conf['HostConfig'])
        if container_ret:
            time.sleep(0.3)
            return (container_ret['Id'])
        else:
            print("Can not create container")
            return

    def start_container(self,node_ip,node_port,container_id):
        if len(container_id) > 0:
            container_ip = ""
            client_ins = docker.Client(base_url='tcp://' + node_ip + ":" + node_port, version='1.20', timeout=5)
            client_ins.start(container_id)
            time.sleep(0.5)
            con_info = self._container_detail(node_ip, node_port,container_id)
            ret = NodeInfo.get_con_usage_info(container_id,node_ip)
            print(ret)
            if len(ret) == 0:
                NodeInfo.insert_con_usage(container_id[0:12],con_info['NetworkSettings']['IPAddress'],con_info['Name'].replace('/',''),node_ip)
            else:
<<<<<<< HEAD
                #print('update_con_usage')
                #print(con_info['NetworkSettings']['IPAddress'], con_info['Name'].replace('/', ''), node_ip, container_id[0:12])
                NodeInfo.update_con_usage(container_id[0:12],con_info['NetworkSettings']['IPAddress'],con_info['Name'].replace('/',''),node_ip)
=======
                #print(con_info['NetworkSettings']['IPAddress'], con_info['Name'].replace('/', ''), node_ip, container_id[0:12    ])
                NodeInfo.update_con_usage(container_id[0:12],con_info['NetworkSettings']['IPAddress'],con_info['Name'].replac    e('/',''),node_ip)
>>>>>>> e112b4fb623db7a3307db4b020b09b1f466ee07a
            return 0
        else:
            print("Please enter the Container ID")
            return

    def container_info(self, node_ip, node_port, container_id):
        con_data = {}
        tmp_dict = {}
        ip_ret = ""
        ret_json = self._container_detail(node_ip, node_port, container_id)
        if len(ret_json) < 1:
            return con_data

        con_state = ""
        if ('Running' in ret_json['State'].keys()) and ('Status' not in ret_json['State'].keys()):  # for docker 1.7
            con_state = str(ret_json['State']['Running'])
        elif 'Status' in ret_json['State'].keys():  # for docker 1.9 and higher
            con_state = str(ret_json['State']['Status'])
        else:  # for else
            con_state = "Exited"
        tmp_dict['id_num'] = ret_json['Id'][0:12]
        tmp_dict['node_ip'] = node_ip
        tmp_dict['con_ip'] = ret_json['NetworkSettings']['IPAddress']
        tmp_dict['name'] = ret_json['Name'].replace('/','')
        tmp_dict['image'] = ret_json['Image']
        tmp_dict['created'] = ret_json['State']['StartedAt']
        tmp_dict['state'] = con_state
        tmp_dict['memory'] = ret_json['HostConfig']['Memory']
        tmp_dict['cpuperiod'] = ret_json['HostConfig']['CpuPeriod']
        tmp_dict['cpuquota'] = ret_json['HostConfig']['CpuQuota']
        tmp_dict['hostname'] = str(ret_json['Config']['Hostname'])
        tmp_dict['cmd'] = str(ret_json['Config']['Cmd'])
        con_data[1] = tmp_dict
        return con_data

    def stop_container(self, node_ip, node_port, container_id):
        if len(container_id) > 0:
            print("      Stop the container %s ........" % container_id)
            client_ins = docker.Client(base_url='tcp://' + node_ip + ":"
                                                + node_port, version='1.20', timeout=5)
            client_ins.stop(container_id)
        else:
            print("Please enter the Container ID")
            return

    def destroy_container(self, node_ip, node_port, container_id):
        if len(container_id) > 0:
            print("      Destroy the container %s ....... " % container_id)
            client_ins = docker.Client(base_url='tcp://' + node_ip + ':'
                                                + node_port, version='1.20', timeout=5)
            try:
                client_ins.stop(container_id)
                time.sleep(0.3)
                client_ins.remove_container(container_id)
                time.sleep(0.3)
            except docker.errors.NotFound:
                print("      NO Such container id")
            self.delete_con_usage(container_id)
        else:
            print("Please enter the Container ID")
            return 1

    def node_info(self,node_ip, node_port):
        url = ('http://' + node_ip + ":" + node_port + "/info")
        node_more_url = Curl(url)
        ret_json = node_more_url.get_value()
        return ret_json

def main_node_info():
    myswarm = Myswarm()
    #for image in myswarm.images_list("172.16.1.101","2375"):
    #    print(image)
    node_info = myswarm.node_info("172.16.1.101","2375")
    print(node_info["Name"])
    #print(node_ip)
    #print(port)
    print(node_info["NCPU"])
    print(node_info["MemTotal"])
    print(node_info["Images"])
    #print(node_info["state"])
    #print(node_group)
    print(node_info["Containers"])
    print(node_info["OperatingSystem"])
    print(node_info["PkgVersion"])
    print(node_info["KernelVersion"])

def main_con_info():
    myswarm = Myswarm()
    node_ip = "172.16.1.101"
    port = "2375"
    con_data = myswarm.container_list(node_ip,port)
    for con in con_data:
        print(con_data[con]["id_num"],con_data[con]["con_ip"],con_data[con]["con_name"],node_ip)

if __name__ == '__main__':
    main_con_info()
