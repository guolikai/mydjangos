#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Guolikai


import datetime
import os
import sys
import json
import time
import subprocess
import re
import requests
from conf import settings

# python2 utf8格式加载
# reload(sys)
# sys.setdefaultencoding('utf-8')

##自定义变量
Today = time.strftime("%Y%m%d%H%M%S")
Now_Stamp = int(time.time())

#linux执行shell命令
class LinuxOSCommand(object):
    def __init__(self,command):
        self.command = command

    def linux_os_command(self):
        result=[]
        cmd_res = subprocess.getstatusoutput(self.command)
        #print(cmd_res)    #返回的结果是一个元组
        for item in cmd_res[1].split("\n"):
            result.append(item)
        return result
        
def print_list_exec(list1):
    return json.dumps(list1,encoding="UTF-8",ensure_ascii=False)

def string_unicode_to_utf8(str):
    # str = 'argo: \\u672a\\u627e\\u5230\\u547d\\u4ee4'
    # print type(str),str.decode('unicode_escape')
    return str.decode('unicode_escape')

def unicode_to_utf8_dict(dict):
    dict1 = json.dumps(dict)
    dict2 = dict1.decode("unicode-escape").decode("unicode-escape")
    return dict2

def string_remove_space(string):
    ## \S匹配任何非空白字符，它相当于类[^\t\n\r\f\v]
    new_list = re.findall("\S+", string)
    new_string = ""+" ".join(new_list)+""
    data = {"list":new_list,"string":new_string}
    return data
 

def unicode_convert(input):
    if isinstance(input, dict):
        return {unicode_convert(key): unicode_convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [unicode_convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


def json_save_to_txt(data):
    ### json.dumps()方法会默认将其中unicode码以ascii编码的方式输入到string
    ### indent = 4   代表按格式缩进4个空格
    ### ensure_ascii = False   对于非ascii字符不采用ascii编码，可以处理中文乱码问题
    with open(dist_file, "w") as fp:
        fp.write(json.dumps(data, ensure_ascii=False,indent=4))
        #fp.write(json.dumps(data, ensure_ascii=False))


def json_read_from_txt(dist_file):
    try:
        with open(dist_file, 'r',) as f:
            # Unicode编码
            data = json.loads(f.read())
            # Unicode编码转化为UTF8中文编码读
            # data = json.dumps(data, encoding="UTF-8", ensure_ascii=False)
            # print (data)
    except ValueError:
        sys.exit()
    except IOError:
        print(dist_file+"文件不存在")
        sys.exit()
    return data
    
### 文件重命名
def file_rename(srcFile,dstFile):
    try:
        os.rename(srcFile,dstFile)
    except Exception as e:
        print(e)
        print(srcFile + ' rename file fail\r\n')
    else:
        print(srcFile + ' rename file success\r\n')
