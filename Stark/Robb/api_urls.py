#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Created on 2017-5-23 by Author:GuoLikai

from django.conf.urls import url,include
from Robb import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'client/config/(\d+)$',views.client_configs),
    url(r'client/service/report/$',views.service_data_report),
    url(r'hosts/status/$', views.hosts_status, name='get_hosts_status'),
    url(r'groups/status/$', views.hostgroups_status, name='get_hostgroups_status'),
    url(r'graphs/$', views.graphs_generator, name='get_graphs')
]