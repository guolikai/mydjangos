#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Created on 2017-5-23 by Author:GuoLikai
#http://www.cnblogs.com/alex3714/articles/5450798.html

from django.db import models
from Wolf.models import UserProfile
# Create your models here.

class Host(models.Model):
    name =  models.CharField(max_length=64,unique=True)
    ip_addr =  models.GenericIPAddressField(unique=True)
    host_groups = models.ManyToManyField('HostGroup',blank=True) # A B C
    templates = models.ManyToManyField("Template",blank=True) # A D E
    monitored_by_choices = (
        ('agent','Agent'),
        ('snmp','SNMP'),
        ('wget','WGET'),
    )
    monitored_by = models.CharField(u'监控方式',max_length=64,choices=monitored_by_choices)
    status_choices= (
        (1,'Online'),
        (2,'Down'),
        (3,'Unreachable'),
        (4,'Offline'),
        (5,'Problem'),
    )
    host_alive = models.IntegerField(u'主机状态存活间隔',default=30)
    status = models.IntegerField(u'状态',choices=status_choices,default=1)
    memo = models.TextField(u"备注",blank=True,null=True)
    def __str__(self):
        return self.name

class HostGroup(models.Model):
    name =  models.CharField(max_length=64,unique=True)
    templates = models.ManyToManyField("Template",blank=True)
    memo = models.TextField(u"备注",blank=True,null=True)
    def __str__(self):
        return self.name

class ServiceIndex(models.Model):
    name = models.CharField(max_length=64)  #idle
    key =models.CharField(max_length=64)    #idle的key，与客户端一致
    data_type_choices = (
        ('int',"int"),
        ('float',"float"),
        ('str',"string")
    )
    data_type = models.CharField(u'指标数据类型',max_length=32,choices=data_type_choices,default='int')
    memo = models.CharField(u"备注",max_length=128,blank=True,null=True)
    def __str__(self):
        return "%s.%s" %(self.name,self.key)

class Service(models.Model):
    name = models.CharField(u'服务名称',max_length=64,unique=True)
    interval = models.IntegerField(u'监控间隔',default=60)
    plugin_name = models.CharField(u'插件名',max_length=64,default='n/a')
    items = models.ManyToManyField('ServiceIndex',verbose_name=u"指标列表",blank=True)
    has_sub_service = models.BooleanField(default=False,help_text=u'如果一个服务还有独立的子服务，选择这个；比如网卡有多个独立的子网卡')
    memo = models.CharField(u"备注",max_length=128,blank=True,null=True)

    def __str__(self):
        return self.name
    #def get_service_items(obj):
    #    return ",".join([i.name for i in obj.items.all()])

class Template(models.Model):
    name = models.CharField(u'模版名称',max_length=64,unique=True)
    services = models.ManyToManyField('Service',verbose_name=u"服务列表")
    triggers = models.ManyToManyField('Trigger',verbose_name=u"触发器列表",blank=True)
    def __str__(self):
        return self.name

class TriggerExpression(models.Model):
    #name = models.CharField(u"触发器表达式名称",max_length=64,blank=True,null=True)
    trigger = models.ForeignKey('Trigger',verbose_name=u"所属触发器")
    service = models.ForeignKey(Service,verbose_name=u"关联服务")
    service_index = models.ForeignKey(ServiceIndex,verbose_name=u"关联服务指标")
    specified_index_key = models.CharField(verbose_name=u"只监控专门指定的指标key",max_length=64,blank=True,null=True)
    operator_type_choices = (('eq','='),('lt','<'),('gt','>'))
    operator_type = models.CharField(u"运算符",choices=operator_type_choices,max_length=32)
    data_calc_type_choices = (
        ('avg','Average'),
        ('max','Max'),
        ('hit','Hit'),
        ('last','Last'),
    )
    data_calc_func= models.CharField(u"数据处理方式",choices=data_calc_type_choices,max_length=64)
    data_calc_args = models.CharField(u"函数传入参数",help_text=u"若是多个参数,则用,号分开,第一个值是时间",max_length=64)
    threshold = models.IntegerField(u"阈值")

    logic_type_choices = (('or','OR'),('and','AND'))
    logic_type = models.CharField(u"与一个条件的逻辑关系",choices=logic_type_choices,max_length=32,blank=True,null=True)
    #next_condition = models.ForeignKey('self',verbose_name=u"右边条件",blank=True,null=True,related_name='right_sibling_condition' )
    def __str__(self):
        return "%s %s(%s(%s))" %(self.service_index,self.operator_type,self.data_calc_func,self.data_calc_args)
    class Meta:
        pass #unique_together = ('trigger_id','service')

class Trigger(models.Model):
    name = models.CharField(u'触发器名称',max_length=64)
    #expressions= models.TextField(u"表达式")
    severity_choices = (
        (1,'Information'),
        (2,'Warning'),
        (3,'Average'),
        (4,'High'),
        (5,'Disaster'),
    )
    #expressions = models.ManyToManyField(TriggerExpression,verbose_name=u"条件表达式")
    severity = models.IntegerField(u'告警级别',choices=severity_choices)
    enabled = models.BooleanField(default=True)
    memo = models.TextField(u"备注",blank=True,null=True)

    def __str__(self):
        return "<serice:%s, severity:%s>" %(self.name,self.get_severity_display())

class Action(models.Model):
    name =  models.CharField(max_length=64,unique=True)
    host_groups = models.ManyToManyField('HostGroup',blank=True)
    hosts = models.ManyToManyField('Host',blank=True)
    triggers = models.ManyToManyField('Trigger',blank=True,help_text=u'想让哪些Trigger出发当前')
    interval = models.IntegerField(u'告警间隔(s)',default=300)
    operations = models.ManyToManyField('ActionOperation')

    recover_notice = models.BooleanField(u'故障恢复后发送通知消息',default=True)
    recover_subject = models.CharField(max_length=128,blank=True,null=True)
    recover_message = models.TextField(blank=True,null=True)

    enabled = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class ActionOperation(models.Model):
    name =  models.CharField(max_length=64)
    step = models.SmallIntegerField(u"第n次告警",default=1)
    action_type_choices = (
        ('email','Email'),
        ('sms','SMS'),
        ('script','RunScript'),
    )
    action_type = models.CharField(u"动作类型",choices=action_type_choices,default='email',max_length=64)
    notifiers= models.ManyToManyField(UserProfile,verbose_name=u"通知对象",blank=True)
    _msg_format = '''Host({hostname},{ip}) service({service_name}) has issue,msg:{msg}'''  #_msg_format私有变量
    msg_format = models.TextField(u'消息格式',default=_msg_format)
    def __str__(self):
        return self.name

class Maintenance(models.Model):
    #主机维护，本段时间内告警不报
    name =  models.CharField(max_length=64,unique=True)
    hosts = models.ManyToManyField('Host',blank=True)
    host_groups = models.ManyToManyField('HostGroup',blank=True)
    content = models.TextField(u"维护内容")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    def __str__(self):
        return self.name

class EventLog(models.Model):
    """存储报警及其它事件日志"""
    event_type_choices = ((0, '报警事件'), (1, '维护事件'))
    event_type = models.SmallIntegerField(choices=event_type_choices, default=0)
    host = models.ForeignKey("Host")
    trigger = models.ForeignKey("Trigger", blank=True, null=True)
    log = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return "host%s  %s" % (self.host, self.log)

'''
1、监控信息：
CPU
    idle 80
    usage  90
    system  30
    user 20
    iowait  50
memory
    usage
    free
    swap
    cache
    buffer
2、主机 模板
h1 = {
    template:[template1,template2]
    groups:[g1,g2]
}
3、Trigger表达式
h1 h2
    cpu.idle(hit(5 3)) < 10% and
    cpu.iowait(avg(5)) < 30% or
    linux.mem_free(avg(10)) < 15%
severity: warning
4、Trigges
operations
    trigger1,trigger1
    actions = {
        action1,
        action2,
        action3,
    }
5、Actions
actions
    action1:{
        step:5,
        email:,
        to_who:[u1,u2]
    },
    action2:{
        step:10,
        sms:,
        to_who:[u3,u4]
    },
    action3:{
        step:15,
        eweichat:,
        to_who:[u5]
    }
'''