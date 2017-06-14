#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Created on 2017-5-23 by Author:GuoLikai

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render,HttpResponse
import json,time
from Robb.backends import redis_conn
from Robb.backends import data_optimization
from Robb.backends import data_processing
#from Robb.serializer import ClientHandler
#from Robb.serializer import get_host_triggers
from django.shortcuts import render,HttpResponse
from Robb import models,serializer
from Stark import settings

# Create your views here.
REDIS_OBJ = redis_conn.redis_conn(settings)

# Create your views here.
def index(request):
    return render(request,'Robb/monitor/index.html')

def dashboard(request):
    return render(request,'Robb/monitor/dashboard.html')

def triggers(request):
    return render(request,'Robb/monitor/triggers.html')

def hosts(request):
    host_list = models.Host.objects.all()
    print("hosts:",host_list)
    return render(request,'Robb/monitor/hosts.html',{'host_list':host_list})

def host_detail(request,host_id):
    host_obj = models.Host.objects.get(id=host_id)
    return render(request,'Robb/monitor/host_detail.html', {'host_obj':host_obj})

def hosts_status(request):
    hosts_data_serializer = serializer.StatusSerializer(request,REDIS_OBJ)
    hosts_data = hosts_data_serializer.by_hosts()
    return HttpResponse(json.dumps(hosts_data))

def hostgroups_status(request):
    group_serializer = serializer.GroupStatusSerializer(request,REDIS_OBJ)
    group_serializer.get_all_groups_status()
    return HttpResponse('ss')

def client_configs(request,client_id):
    #print("--->Client_id",client_id)
    config_obj = serializer.ClientHandler(client_id)
    config = config_obj.fetch_configs()
    if config:
        return HttpResponse(json.dumps(config))

@csrf_exempt
def service_data_report(request):
    #print("Client report data--->", request.POST)
    if request.method == 'POST':
        #print("Client report data--->",request.POST)
        #REDIS_OBJ.set("test_glk",'hahaha')
        try:
            print(u'客户端监控信息: host=%s, service=%s' %(request.POST.get('client_id'),request.POST.get('service_name') ) )
            data = json.loads(request.POST['data'])
            #print(data)
            #print(type(data))
            #StatusData_1_memory_latest
            client_id = request.POST.get('client_id')
            service_name = request.POST.get('service_name')

            #客户端数据优化与存储
            data_saveing_obj = data_optimization.DataStore(client_id,service_name,data,REDIS_OBJ)
            redis_key_format = "StatusData_%s_%s_latest" %(client_id,service_name)
            #data['report_time'] = time.time()
            #REDIS_OBJ.lpush(redis_key_format,json.dumps(data))

            #在这里同时触发监控
            host_obj = models.Host.objects.get(id=client_id)
            #print(host_obj)
            service_triggers = serializer.get_host_triggers(host_obj)
            #print("触发器ServiceTriggers:", service_triggers)

            trigger_handler = data_processing.DataHandler(settings,connect_redis=False)
            for trigger in service_triggers:
                trigger_handler.load_service_data_and_calulating(host_obj,trigger,REDIS_OBJ)

            #更改主机存活状态
            #host_alive_key = "HostAliveFlag_%s" % client_id
            #REDIS_OBJ.set(host_alive_key,time.time())
        except IndexError as e:
            print('-->service_data_report err:',e)
    return HttpResponse(json.dumps("---report success---"))

def graphs_generator(request):
    graphs_generator = graphs.GraphGenerator2(request,REDIS_OBJ)
    graphs_data = graphs_generator.get_host_graph()
    print("graphs_data",graphs_data)
    return HttpResponse(json.dumps(graphs_data))

def graph_bak(request):
    #host_id = request.GET.get('host_id')
    #service_key = request.GET.get('service_key')
    #print("graph:", host_id,service_key)
    graph_generator = graphs.GraphGenerator(request,REDIS_OBJ)
    graph_data = graph_generator.get_graph_data()
    if graph_data:
        return HttpResponse(json.dumps(graph_data))

def trigger_list(request):
    host_id = request.GET.get("by_host_id")
    host_obj = models.Host.objects.get(id=host_id)
    alert_list = host_obj.eventlog_set.all().order_by('-date')
    return render(request,'Robb/monitor/trigger_list.html',locals())

def host_groups(request):
    host_groups = models.HostGroup.objects.all()
    return render(request,'Robb/monitor/host_groups.html',locals())