#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Created on 2017-5-23 by Author:GuoLikai

import hashlib,time

def get_token(username,token_id):
    timestamp = int(time.time())  #返回当前时间的时间戳（1970纪元后经过的浮点秒数）
    md5_format_str = "%s\n%s\n%s" %(username,timestamp,token_id)
    obj = hashlib.md5()
    #obj.update(md5_format_str.encode(encoding='gb2312')) #更新哈希对象以字符串参数
    obj.update(md5_format_str.encode())
    #http://blog.csdn.net/beiji_nanji/article/details/7486894
    #中文字符在Python中是以unicode存在的,同一个字符串在不同的编码体系下有不同的值
    #所以在hash前要进行编码，个人建议转为gb2312,因为对比发现，我下载的一个工具算出的md5值是与gb2312编码后算出的md5值一样;
    #print("token format:[%s]" % md5_format_str)
    #print("token :[%s]" % obj.hexdigest())   #obj.hexdigest()返回摘要，作为十六进制数据字符串值,
    return(obj.hexdigest()[10:17], timestamp)

if __name__ =='__main__':
    print(get_token('admin','test'))