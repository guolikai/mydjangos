#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Created on 2017-5-23 by Author:GuoLikai

from django.contrib import admin
from Robb import models
# Register your models here.
class HostAdmin(admin.ModelAdmin):
    # 在Django的admin中，通过制定list_display即可制定实体显示出来的字段，但是如果想添加一个新的不是实体有的字段
    # 指定在列表中视图中展现的字段
    list_display = ('name','ip_addr','status')
    filter_horizontal = ('host_groups','templates')
    # 指定搜索的字段
    search_fields = ('name',)

class HostGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)

class TemplateAdmin(admin.ModelAdmin):
    filter_horizontal = ('services', 'triggers')

class ServiceAdmin(admin.ModelAdmin):
    filter_horizontal = ('items',)
    list_display = ( 'name', 'interval', 'plugin_name')
    #list_select_related = ('items')

class TriggerExpressionInline(admin.TabularInline):
    model = models.TriggerExpression
    #exclude = ('memo',)
    #readonly_fields = ['create_date']
class TriggerAdmin(admin.ModelAdmin):
    list_display = ('name', 'severity', 'enabled')
    inlines = [TriggerExpressionInline,]
    #filter_horizontal = ('expressions')
class TriggerExpressionAdmin(admin.ModelAdmin):
    list_display = ('trigger', 'service', 'service_index','specified_index_key')

admin.site.register(models.Host,HostAdmin)
admin.site.register(models.HostGroup,HostGroupAdmin)
admin.site.register(models.Template,TemplateAdmin)
admin.site.register(models.Service,ServiceAdmin)
admin.site.register(models.Trigger,TriggerAdmin)
admin.site.register(models.TriggerExpression,TriggerExpressionAdmin)
admin.site.register(models.ServiceIndex)
admin.site.register(models.Action)
admin.site.register(models.ActionOperation)
admin.site.register(models.Maintenance)
admin.site.register(models.EventLog)