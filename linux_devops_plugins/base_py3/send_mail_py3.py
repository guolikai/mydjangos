#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#----------------------------------------------------------------------
#Name:        send_mail_python3.py
#Version:     v1.0
#Create_Date：2017-12-12
#Author:      GuoLikai(glk73748196@sina.com)
#Description: "Send Mail Script from 163.com"
#----------------------------------------------------------------------

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

class SendMail(object):
    def __init__(self,maillist,mailtitle,mailcontent):
        self.mail_list = maillist
        self.mail_title = mailtitle
        self.mail_content = mailcontent

        #self.mail_host = "smtp.163.com"
        #self.mail_user = "glk0518@163.com"
        #self.mail_pass = "shouquan163"
        #self.mail_postfix = "163.com"

        self.mail_host = "smtp.yanxiu.com"
        #self.mail_user = "zabbix@yanxiu.com"
        #self.mail_pass = "srt123"
        self.mail_user = "system@yanxiu.com"
        self.mail_pass = "Yx@srt2015*"
        self.mail_postfix = "yanxiu.com"
        #print(self.mail_host,self.mail_user,self.mail_pass,self.mail_list)


    def SendMail(self):
        me = self.mail_user + "<" + self.mail_user + "@" + self.mail_postfix + ">"
        msg = MIMEMultipart()
        msg['Subject'] = self.mail_title
        msg['From'] = me
        msg['To'] = ";".join(self.mail_list)

        #纯文本内容
        #puretext = MIMEText('<h1>你好，<br/>'+self.mail_content+'</h1>','html','utf-8')
        #puretext = MIMEText('纯文本内容'+self.mail_content)
        puretext = MIMEText(self.mail_content)
        msg.attach(puretext)

        #jpg类型的附件
        jpgpart = MIMEApplication(open('/root/workspace/python-dev/dbcount/templates/static/images/logo.jpg', 'rb').read())
        jpgpart.add_header('Content-Disposition', 'attachment', filename='logo.jpg')
        msg.attach(jpgpart)

        # xlsx类型的附件
        #xlsxpart = MIMEApplication(open('/root/workspace/backup/mysql-analy/mysql_analy_2017-12-12_top10.xls', 'rb').read())
        #xlsxpart.add_header('Content-Disposition', 'attachment', filename='mysql_analy_2017-12-12_top10.xls')
        #msg.attach(xlsxpart)

        # mp3类型的附件
        #mp3part = MIMEApplication(open('kenny.mp3', 'rb').read())
        #mp3part.add_header('Content-Disposition', 'attachment', filename='benny.mp3')
        #msg.attach(mp3part)

        # pdf类型附件
        #part = MIMEApplication(open('foo.pdf', 'rb').read())
        #part.add_header('Content-Disposition', 'attachment', filename="foo.pdf")
        #msg.attach(part)

        try:
            s = smtplib.SMTP()                                #创建邮件服务器对象
            s.connect(self.mail_host)                         #连接到指定的smtp服务器。参数分别表示smpt主机和端口
            s.login(self.mail_user, self.mail_pass)           #登录到你邮箱
            s.sendmail(me,self.mail_list, msg.as_string())   #发送内容
            s.close()
            return True
        except Exception as e:
            print(e)
            return False

    def SendMailMain(self,Filedir,File):
        me = self.mail_user + "<" + self.mail_user + "@" + self.mail_postfix + ">"
        msg = MIMEMultipart()
        msg['Subject'] = self.mail_title
        msg['From'] = me
        msg['To'] = ";".join(self.mail_list)
        puretext = MIMEText(self.mail_content)
        msg.attach(puretext)
        #print('/root/workspace/backup/mysql-analy/mysql_analy_2017-12-12_top10.xls', 'rb')
        Attachment="%s/%s" % (Filedir,File)
        attachmentpart = MIMEApplication(open(Attachment, 'rb').read())
        attachmentpart.add_header('Content-Disposition', 'attachment', filename='%s' % File)
        msg.attach(attachmentpart)
        try:
            s = smtplib.SMTP()                                #创建邮件服务器对象
            s.connect(self.mail_host)                         #连接到指定的smtp服务器。参数分别表示smpt主机和端口
            s.login(self.mail_user, self.mail_pass)           #登录到你邮箱
            s.sendmail(me,self.mail_list,msg.as_string())     #发送内容
            s.close()
            return True
        except Exception as e:
            print(e)
            return False

def main():
    #send list
    mailto_list = ["glk0518@163.com"]
    mail_title = 'Hey subject'
    mail_content = 'Hey this is content'
    send_mail = SendMail(mailto_list,mail_title,mail_content)
    send_res = send_mail.SendMail()
    print(send_res)


def sendmain(num):
    #send list
    import datetime
    Today = datetime.date.today()
    Yesterday = Today - datetime.timedelta(days=1)
    mailto_list = ["guolikai@yanxiu.com"]
    mail_title = '数据库分析:Mysql Analyse %s'  % Today
    mail_content = '%s数据库最大的%s张库和表:见附件' % (Yesterday,num)
    mail_attachment_dir = '/root/workspace/backup/mysql-analy'
    mail_attachment_file = 'mysql_analyse_%s_top%s.xls' % (Yesterday,num)
    send_mail = SendMail(mailto_list,mail_title,mail_content)
    send_res = send_mail.SendMailMain(mail_attachment_dir,mail_attachment_file)
    print(send_res)

def sendmailfile(num,mail_attachment_dir,mail_attachment_file):
    #send list
    import datetime
    Today = datetime.date.today()
    Yesterday = Today - datetime.timedelta(days=1)
    mailto_list = ["guolikai@yanxiu.com"]
    mail_title = '数据库分析:Mysql Analyse %s'  % Today
    mail_content = '%s数据库最大的%s张库和表:见附件' % (Yesterday,num)
    #mail_attachment_dir = '/root/workspace/backup/mysql-analy'
    #mail_attachment_file = 'mysql_analyse_%s_top%s.xls' % (Yesterday,num)
    send_mail = SendMail(mailto_list,mail_title,mail_content)
    send_res = send_mail.SendMailMain(mail_attachment_dir,mail_attachment_file)
    if send_res:
        print("'%s'邮件发送成功!" % mail_title)
    


if __name__ == '__main__':
    #main()
    num=100
    sendmain(num)
