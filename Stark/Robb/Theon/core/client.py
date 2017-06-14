#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Created on 2017-5-26 by Author:GuoLikai

import json,time,urllib,threading,os,sys
import urllib.parse
import urllib.request
from conf import settings
from plugins import plugin_api

class ClientHandle(object):
    def __init__(self):
        self.monitored_services = {}

    def load_latest_config(self):
        '''
        load the latest monitor config from monitor server
        :return:
        '''
        request_type = settings.configs['urls']['get_configs'][1]
        url = "%s/%s"  % (settings.configs['urls']['get_configs'][0],settings.configs['HostID'])
        latest_configs = self.url_request(request_type,url)
        latest_configs = json.loads(latest_configs.decode())   #json.load的对象必须是str
        self.monitored_services.update(latest_configs)    #字典里的用法；
        #print('---monitored_services--->',self.monitored_services)


    def forever_run(self):
        '''
        Start the Client program forever
        :return:
        '''
        exit_flag = False
        config_last_update_time = 0
        while not exit_flag:
            if time.time() - config_last_update_time > settings.configs['ConfUpdateInterval']:
                self.load_latest_config()
                #print("Load latest config:",self.monitored_services)
                config_last_update_time = time.time()
                #Start  to monitor services
            for service_name,val in self.monitored_services['services'].items():
                if len(val) == 2:   #means it's the first time to monitor
                    self.monitored_services['services'][service_name].append(0)
                    monitor_interval = val[1]
                    last_invoke_time = val[2]
                    if time.time() - last_invoke_time > monitor_interval:
                        #print(last_invoke_time,time.time())
                        self.monitored_services['services'][service_name][2] = time.time()
                        #start a new thread to call each monitor plugin
                        #print(u'Thread参数:',type(service_name),type(val),val)
                        t = threading.Thread(target=self.invoke_plugin,args=(service_name,val))
                        t.start()
                        print("Going to monitor [%s]" % service_name)
                    else:
                        print("Going to monitor [%s] in [%s] secs" %(service_name,monitor_interval-(time.time()-last_invoke_time)))
            time.sleep(0.1)

    def invoke_plugin(self,service_name,val):
        plugin_name = val[0]
        if hasattr(plugin_api,plugin_name):
            func = getattr(plugin_api,plugin_name)
            plugin_callback = func()
            #print("---monitor plugin result--->",plugin_callback)
            #print("---monitor plugin result--->", type(plugin_callback))
            #plugin_callback = str(plugin_callback)   #字典转换为字符串str
            report_data = {
                'client_id':settings.configs['HostID'],
                'service_name':service_name,
                'data':json.dumps(plugin_callback)
            }
            request_action = settings.configs['urls']['service_report'][1]
            request_url = settings.configs['urls']['service_report'][0]
            #print("---report data--->",report_data,request_url,request_action)
            self.url_request(request_action,request_url,params=report_data)
        else:
            print("\033[31,1m Cannot find plugin names [%s] in plugin_api\033[31,0m" % service_name )
        #print("--->插件名:",val)

    def url_request(self,action,url,**extra_data):
        abs_url = "http://%s:%s/%s" % (settings.configs['Server'],
                                        settings.configs['ServerPort'],
                                        url)
        if action in ('get','GET'):
            print('---Get Client Config--->',abs_url,extra_data)
            try:
                req = urllib.request.Request(abs_url)
                req_data = urllib.request.urlopen(req, timeout=settings.configs['RequestTimeout'])
                callback = req_data.read()
                #print(callback)
                return callback
            except urllib.request.URLError as e:
                exit("\033[31;1m%s\033[0m" % e)
        elif action in ('post','POST'):
            print('---POST Client Data--->',action,abs_url,extra_data)
            try:
                data_encode = urllib.parse.urlencode(extra_data['params']).encode()
                #print(data_encode)
                req = urllib.request.Request(url=abs_url, data=data_encode)
                res_data = urllib.request.urlopen(req, timeout=settings.configs['RequestTimeout'])
                #callback = res_data.read()
                callback = res_data.read().decode()  # 字符转换成字符串
                #print('callback',type(callback.decode()))
                callback = json.loads(callback)
                # print("---> \033[31;1m[%s]:[%s]\033[0m response:\n%s" %(action,abs_url,callback))
                return callback
            except Exception as e:
                print("---exec",e)
                exit("\033[31;1m%s\033[0m" % e)