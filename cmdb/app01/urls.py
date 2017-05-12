"""HostMangerDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from app01 import views
urlpatterns = [
    url(r'^$', views.Login),
    url(r'^login/$', views.Login),
    url(r'^logout/$', views.Logout),
    url(r'^register', views.Register),
    url(r'^index', views.Index),
    url(r'^host_list/(\d*)', views.Host_list),
    url(r'^host_add', views.host_add),
    url(r'^host_del', views.host_del),
    url(r'^host_mod', views.host_mod),
    url(r'^type_add', views.type_add),
    url(r'^type_del', views.type_del),
    url(r'^type_mod', views.type_mod),
    url(r'^type_get', views.type_get),
    url(r'^user_add', views.user_add),
    url(r'^user_del', views.user_del),
    url(r'^user_get', views.user_get),
    url(r'^user_mod', views.user_mod),
    url(r'^group_add', views.group_add),
    url(r'^group_get', views.group_get),
    url(r'^group_del', views.group_del),
    url(r'^group_mod', views.group_mod),
]
