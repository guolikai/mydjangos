#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Created on 2017-5-5  by Author:GuoLikai

import os
class BaseSaltModule(object):
    def __init__(self,sys_argvs,db_models,settings):
        self.db_models = db_models
        self.settings = settings
        self.sys_argvs = sys_argvs
    def argv_validation(self,argv_name,val,data_type):
        if type(val) is not data_type:
            exit("Error: [%s]'s data type is not valid" % argv_name)

    def get_selected_os_types(self):
        data = {}
        for host in self.host_list:
            data[host.os_type] = []
        print('--->data',data)
        return data

    def process(self):
        self.fetch_hosts()
        self.config_data_dic = self.get_selected_os_types()
        
    
            
    def is_required(self,*args,**kwargs):
        mod_name = kwargs.get('mod_name')
        mod_val = kwargs.get('mod_val')
        #print("mod_name[%s]  mod_val[%s]" % (mod_name,mod_val))
        print("Error: is_required() method must be implemented in module class [%s]" % args[0])
        
    def require(self,*args,**kwargs):
        #print('--In Require',args,kwargs)
        os_type = kwargs.get('os_type')
        self.require_list = []
        for item in args[0]:
            for mod_name,mod_val in item.items():
                module_obj = self.get_module_instance(base_mod_name=mod_name,os_type=os_type)
                #print('Require run module:',module_obj)
                require_condition = module_obj.is_required(mod_name,mod_val)
                self.require_list.append(require_condition)
        #print('---> Require_list',self.require_list)
    
    def get_module_instance(self,*args,**kwargs):
        base_mod_name = kwargs.get('base_mod_name')
        os_type = kwargs.get('os_type')
        plugin_file_path = "%s/%s.py" % (self.settings.SALT_PLUGINS_DIR,base_mod_name)
        #print(plugin_file_path) 
        if os.path.isfile(plugin_file_path):
            #导入 模块
            module_plugin = __import__('plugins.%s' % base_mod_name)
            special_os_module_name = "%s%s" %(os_type.capitalize(),base_mod_name.capitalize())
            module_file= getattr(module_plugin,base_mod_name) # 这里才是真正导入模块
            if hasattr(module_file, special_os_module_name): #判断有没有根据操作系统的类型进行特殊解析 的类，在这个文件里
                module_instance = getattr(module_file, special_os_module_name)
            else:
                module_instance = getattr(module_file,base_mod_name.capitalize())               
            #开始调用 此module 进行配置解析                
            module_obj = module_instance(self.sys_argvs,self.db_models,self.settings)
            #module_obj.syntax_parser(section_name,mod_name,mod_data)  #解析user、group.present
            return module_obj   
        else:
            exit("module [%s] is not exist" % base_mod_name)   
        
    def fetch_hosts(self):
        print('--fetching hosts---')

        if '-h' in self.sys_argvs or '-g' in self.sys_argvs:
            host_list = []
            if '-h' in self.sys_argvs:
                host_str_index = self.sys_argvs.index('-h') +1
                if len(self.sys_argvs) <= host_str_index:
                    exit("host argument must be provided after -h")
                else: #get the host str
                    host_str = self.sys_argvs[host_str_index]
                    host_str_list = host_str.split(',')
                    host_list += self.db_models.Host.objects.filter(hostname__in=host_str_list)
            if '-g' in self.sys_argvs:
                group_str_index = self.sys_argvs.index('-g') +1
                if len(self.sys_argvs) <= group_str_index:
                    exit("group argument must be provided after -g")
                else: #get the group str
                    group_str = self.sys_argvs[group_str_index]
                    group_str_list = group_str.split(',')
                    group_list = self.db_models.HostGroup.objects.filter(name__in=group_str_list)
                    for group in group_list:
                        host_list += group.hosts.select_related()
            self.host_list = set(host_list)  #主机去重，self全局
            #return True
            #print('--->host list:', host_list)
        else:
            exit("host [-h] or group[-g] argument must be provided")

    #任务解析
    def syntax_parser(self,section_name,mod_name,mod_data,os_type):
        #print("---> going to parser state data:",section_name,mod_name)
        self.raw_cmds = []
        self.single_line_cmds = []
        for state_item in mod_data:
            #print("\t",state_item)
            for key,val in state_item.items():
                if hasattr(self,key):
                    state_func = getattr(self,key)
                    state_func(val,section=section_name,os_type=os_type)
                    #print(state_func(val))
                else:
                    exit("Error:module [%s] has no method [%s]" %(mod_name,key))
        else:
                if "." in mod_name:
                    base_mod_name,mod_action = mod_name.split(".")
                    if hasattr(self,mod_action):
                        mod_action_func = getattr(self,mod_action)
                        cmd_list = mod_action_func(section=section_name,mod_data=mod_data)
                        data = {
                            'cmd_list':cmd_list,
                            'require_list':self.require_list
                            }
                        #上面代表一个session里的具体的一个module已经解析完毕
                        return data
                    else:
                        exit("Error:module [%s] has no method [%s]" % (mod_name,mod_action))
                else:
                    exit("Error:module action of [%s] must be supplied" % mod_name)