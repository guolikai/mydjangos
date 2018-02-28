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
    url(r'^login/$',views.acc_login,name='login'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^main/$',views.main,name='main'),
    url(r'^base/$', views.base,name='base'),
    url(r'^groupleft/$',views.groupleft,name='groupleft'),
    url(r'^groupright/$',views.groupright,name='groupright'),
    url(r'^mysqlinfo/$',views.mysqlinfo,name='mysqlinfo'),
    url(r'^mysqlaction/$',views.mysqlaction,name='mysqlaction'),
    url(r'^mysqlmodify/$',views.mysqlmodify,name='mysqlmodify'),
    url(r'^databasesize/$',views.databasesize,name='databasesize'),
    url(r'^tableinfo/$',views.tableinfo,name='tableinfo'),
    url(r'^tablecount/$',views.tablecount,name='tablecount'),
    url(r'^msinfo/$',views.msinfo,name='msinfo'),
    url(r'^promoteslave/$',views.promoteslave,name='.promoteslave'),
	url(r'^$',views.acc_login,name="dashboard"),
]
