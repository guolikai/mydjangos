from django.contrib import admin

# Register your models here.
from app01 import models

class MysqlInfoAdmin(admin.ModelAdmin):
    # 指定在列表中视图中展现的字段
    list_display = ('host','mysql_port','mysql_socket','mysql_remark')
    # 指定搜索的字段
    search_fields = ('mysql_port',)
    # 用于关联另一张表的字段信息
    def host(self,obj):
        return obj.mysql_host.ip
    # 修改要显示的名称
    host.short_description = '主机'

class DatabaseSizeAdmin(admin.ModelAdmin):
    list_display = ('database_name','database_size','port','host','create_date')
    search_fields = ('create_date',)
    def database_name(self,obj):
        return obj.database_info.database_name
    def port(self,obj):
        return obj.database_info.database_mysql.mysql_port
    def host(self,obj):
        return obj.database_info.database_mysql.mysql_host.ip
    # 修改要显示的名称
    # 修改要显示的名称
    database_name.short_description = '数据库名'
    port.short_description = '端口'
    host.short_description = '主机'

class TableCountAdmin(admin.ModelAdmin):
    list_display = ('tablename','table_count','database_name','port','host','create_date')
    search_fields = ('create_date',)
    def tablename(self,obj):
        return obj.table_info.table_name
    def database_name(self,obj):
        return obj.table_info.table_database.database_name
    def port(self,obj):
        return obj.table_info.table_mysql.mysql_port
    def host(self,obj):
        return obj.table_info.table_host.ip
    # 修改要显示的名称
    tablename.short_description = '表名'
    database_name.short_description = '数据库名'
    port.short_description = '端口'
    host.short_description = '主机'


admin.site.register(models.DatabaseSize,DatabaseSizeAdmin)
#admin.site.register(models.MysqlInfo,MysqlInfoAdmin)
admin.site.register(models.TableCount,TableCountAdmin)
