#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Created on 2017-5-26 by Author:GuoLikai
from django.conf.urls import include,url
from Robb import views
urlpatterns = [
    url(r'api/', include('Robb.api_urls')),
    url(r'^$', views.index),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^triggers/$', views.triggers, name='triggers'),
    url(r'hosts/$', views.hosts, name='hosts'),
    #url(r'graph/$', views.graph, name='get_graph'),
    url(r'host_groups/$', views.host_groups, name='host_groups'),
    url(r'hosts/(\d+)/$', views.host_detail, name='host_detail'),
    url(r'trigger_list/$', views.trigger_list, name='trigger_list'),
]