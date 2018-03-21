#!/usr/bin/python
# -*- coding: utf-8 -*-
##################################################
#Name:        alert.py
#Version:     v1.0
#Create_Date：2016-8-20
#Author:      GuoLikai(glk73748196@sina.com)
#Description: "Zabbix SMTP Alert script from 163"
##################################################

import sys
import smtplib
from email.mime.text import MIMEText

#邮件发送列表，发给哪些人
#mailto_list=["glk73748196@sina.com","guolikai@yanxiu.com"]
#设置服务器，用户名、授权口令以及邮箱的后缀
mail_host="smtp.163.com"
mail_user="glk0518@163.com"
mail_pass="shouquan163"
mail_postfix="163.com"

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
    msg['To'] =to_list
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(address, to_list, msg.as_string())
        s.close()
        print "done!"
        return True
    except Exception, e:
        print str(e)
        return False
if __name__ == '__main__':
        send_mail(sys.argv[1], sys.argv[2], sys.argv[3])

