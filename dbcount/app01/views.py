#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Created on 2017-11-15 by Author:GuoLikai

# Create your views here.
import django
from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from django.utils import timezone
#HttpResponseRedirect:参数既可以使用完整的url，也可以是绝对路径。
#HttpReponse返回的直接是内容
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
import json

from app01 import models
from ucenter import models as Umodels

def acc_login(request,*args,**kwargs):
    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')
        #print(username,password)
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            if user.valid_end_time: #设置了end time
                if django.utils.timezone.now() > user.valid_begin_time and django.utils.timezone.now()  < user.valid_end_time:
                    auth.login(request,user)
                    request.session.set_expiry(60*30)
                    #print 'session expires at :',request.session.get_expiry_date()
                    return HttpResponseRedirect('/app01/login')
                else:
                    return render(request, 'ucenter/login.html', {'login_err': 'User account is expired,please contact your IT guy for this!'})
            elif django.utils.timezone.now() > user.valid_begin_time:
                    auth.login(request,user)
                    request.session.set_expiry(60*30)
                    request.session['is_login']={'user':username}
                    return HttpResponseRedirect('/app01/main')
        else:
            return render(request, 'ucenter/login.html', {'login_err': 'Wrong username or password!'})
    else:
        return render(request, 'ucenter/login.html')




#装饰器，需要做登录验证
def outer(func):
    def wrapper(request,*args,**kwargs):
        if not request.session.get('is_login'):
            return redirect('/app01/login')
        else:
            return func(request,*args,**kwargs)
    return wrapper

@outer
def logout(request,*args,**kwargs):
    #销毁session值
    del request.session['is_login']
    print('User exit')
    return HttpResponseRedirect('/')

@outer
def main(request,*args,**kwargs):
    return render(request,'app01/main.html')

@outer
def base(request,*args,**kwargs):
    print(request.session['is_login'])
    user_dict = request.session.get('is_login',None)
    return render(request,'base.html',{'username':user_dict['user']})

@outer
def groupleft(request,*args,**kwargs):
    return render(request,'app01/groupleft.html',)

@outer
def groupright(request,*args,**kwargs):
    user_dict = request.session.get('is_login',None)
    ret = {'status':'','data':'','username':user_dict['user']}
    data = Umodels.UserProfile.objects.all()
    ret['data'] = data
    return render(request,'app01/index.html',ret)

@outer
def mysqlinfo(request,*args,**kwargs):
    user_dict = request.session.get('is_login',None)
    ret = {'status':'','data':'','username':user_dict['user']}
    mysql_data = dict()
    datas = models.MysqlInfo.objects.all().values_list('mysql_host__ip','mysql_port','mysql_socket')
    Len=len(datas)
    num=1
    if num < Len:
        for line in datas:
            tmp_dict = dict()
            tmp_dict['id']= num
            tmp_dict['mysql_ip']= line[0]
            tmp_dict['mysql_port']= line[1]
            tmp_dict['mysql_sock']= line[2]
            tmp_dict['mysql_status']= 'Running'
            mysql_data[num] = tmp_dict
            num += 1
    #print(type(mysql_data),mysql_data)
    ret['data'] = mysql_data
    return render(request,"app01/mysqlinfo.html",ret)

@outer
def mysqlaction(request,*args,**kwargs):
    user_dict = request.session.get('is_login',None)
    ret = {'status':'','data':'','host':'','username':user_dict['user']}
    host = request.GET.get('host',None)
    port = request.GET.get('port',None)
    host_id = models.HostInfo.objects.get(ip=host)
    data = models.MysqlInfo.objects.get(mysql_host_id=host_id,mysql_port=port)
    #print(data.id,data.mysql_port,data.mysql_user,data.mysql_passwd,data.mysql_socket,data.mysql_remark,data.mysql_host_id)
    ret['data'] = data
    ret['host'] = host
    return render(request,"app01/mysqlaction.html",ret)

@outer
def mysqlmodify(request,*args,**kwargs):
    user_dict = request.session.get('is_login',None)
    ret = {'status':'','data':'','host':'','username':user_dict['user']}
    ip = request.GET.get('host',None)
    ret['host'] = ip
    port = request.GET.get('port',None)
    user = request.GET.get('mysql_user',None)
    passwd = request.GET.get('mysql_passwd',None)
    socket = request.GET.get('mysql_socket',None)
    remark = request.GET.get('mysql_remark',None)
    print(ip,port,user,passwd,socket,remark)
    count = models.HostInfo.objects.filter(ip=ip).count()
    if count==0:
        ret['status'] = "主机[%s]数据库[%s]记录不存在"  % (ip,port)
    else:
        host_id = models.HostInfo.objects.get(ip=ip)
        models.MysqlInfo.objects.filter(mysql_host_id=host_id).update(mysql_user=user,
                                                                         mysql_passwd=passwd,
                                                                         mysql_socket=socket,
                                                                         mysql_remark=remark)
        data = models.MysqlInfo.objects.get(mysql_host_id=host_id,mysql_port=port)
        ret['data'] = data
        ret['status'] = '数据库信息修改成功'
    return render(request,"app01/mysqlaction.html",ret)

@outer
def databasesize(request,*args,**kwargs):
    user_dict = request.session.get('is_login',None)
    ret = {'status':'','data':'','username':user_dict['user']}
    mysql_data = dict()
    datas = models.DatabaseSize.objects.all().values_list('id','database_size','database_info__database_name',
                                                          'database_info__database_mysql__mysql_port',
                                                          'database_info__database_mysql__mysql_host__ip',
                                                          'create_date',
                                                          )
    Len=len(datas)
    num=1
    if num < Len:
        for line in datas:
            tmp_dict = dict()
            tmp_dict['id']= line[0]
            tmp_dict['database_size']= line[1]
            tmp_dict['database_name']= line[2]
            tmp_dict['database_port']= line[3]
            tmp_dict['database_host']= line[4]
            tmp_dict['create_date']= line[5]
            mysql_data[line[0]] = tmp_dict
            num += 1
    ret['data'] = mysql_data
    return render(request,'app01/databasesize.html',ret)

@outer
def tableinfo(request,*args,**kwargs):
    user_dict = request.session.get('is_login',None)
    ret = {'status':'','data':'','username':user_dict['user']}
    mysql_data = dict()
    datas = models.TableInfo.objects.all().values_list('id','table_name','table_database__database_name',
                                                      'table_mysql__mysql_port','table_host__ip')

    Len=len(datas)
    num=1
    if num < Len:
        for line in datas:
            tmp_dict = dict()
            tmp_dict['id']= line[0]
            tmp_dict['table_name']= line[1]
            tmp_dict['table_db']= line[2]
            tmp_dict['table_port']= line[3]
            tmp_dict['table_host']= line[4]
            mysql_data[line[0]] = tmp_dict
            num += 1
    ret['data'] = mysql_data
    return render(request,'app01/tableinfo.html',ret)


@outer
def tablecount(request,*args,**kwargs):
    user_dict = request.session.get('is_login',None)
    ret = {'status':'','data':'','username':user_dict['user']}
    mysql_data = dict()
    datas = models.TableCount.objects.all().values_list('id','table_count','table_info__table_name',
                                                          'table_info__table_database__database_name',
                                                          'table_info__table_mysql__mysql_port',
                                                          'table_info__table_host__ip',
                                                          'create_date')
    Len=len(datas)
    num=1
    if num < Len:
        for line in datas:
            tmp_dict = dict()
            tmp_dict['id']= line[0]
            tmp_dict['table_count']= line[1]
            tmp_dict['table_name']= line[2]
            tmp_dict['table_db']= line[3]
            tmp_dict['table_port']= line[4]
            tmp_dict['table_host']= line[5]
            tmp_dict['create_date']= line[6]
            mysql_data[line[0]] = tmp_dict
            num += 1
    ret['data'] = mysql_data
    return render(request,'app01/tablecount.html',ret)

@outer
def msinfo(request,*args,**kwargs):
    ret = {}
    ret['data']='Main Subordinate Info Html Testing'
    return render(request,'app01/msinfo.html',ret)

@outer
def promotesubordinate(request,*args,**kwargs):
    ret = {}
    ret['data']='Promote Subordinate  Html Testing'
    return render(request,'app01/promotesubordinate.html',ret)
