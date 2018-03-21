#!/usr/bin/python
# -*- coding: utf-8 -*-
#-------------------------------------------------
#Name:        alert_send_mail_srt.py
#Version:     v1.0
#Create_Date：2016-8-20
#Author:      GuoLikai
#Description: "SMTP Alert script from yanxiu.com"
#-------------------------------------------------

import sys
import smtplib
from email.mime.text import MIMEText

#邮件发送列表，发给哪些人
mailto_list=["939960191@qq.com"]
#mailto_list=["guolikai@yanxiu.com","zhangqi@yanxiu.com","liuzhihao@yanxiu.com"]
#mailto_list=["guolikai@yanxiu.com","zhangqi@yanxiu.com","tianzheng@yanxiu.com","chenxiao@yanxiu.com"]

#设置服务器，用户名、授权口令以及邮箱的后缀
mail_host="smtp.yanxiu.com"
mail_user="zabbix@yanxiu.com"
mail_pass="srt123"
mail_postfix="yanxiu.com"

#定义send_mail函数
def send_mail(to_list,sub,content):
    '''
    to_list:发给谁
    sub:主题
    content:内容
    send_mail("123456789@qq.com","sub","content")
    '''
    address=mail_user+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content)
    msg['Subject'] = sub
    msg['From'] = address
    msg['To'] =','.join(to_list)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(address, to_list, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False
if __name__ == '__main__':
    send_mail(mailto_list, sys.argv[1], sys.argv[2])
