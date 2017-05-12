from django.contrib import admin

# Register your models here.
from app01 import models

class UserTypeAdmin(admin.ModelAdmin):
    #在Django的admin中，通过制定list_display即可制定实体显示出来的字段，但是如果想添加一个新的不是实体有的字段
    # 指定在列表中视图中展现的字段
    list_display = ('typename',)
    # 指定搜索的字段
    search_fields = ('typename',)

class AssetAdmin(admin.ModelAdmin):
    # 指定在列表中视图中展现的字段
    list_display = ('hostname','ip','create_date','update_date','groupname')
    # 指定搜索的字段
    search_fields = ('hostname',)
    # 用于关联另一张表的字段信息
    def groupname(self,obj):
        return obj.user_group.groupname
    # 修改要显示的名称
    groupname.short_description = '用户组'

class UserGroupAdmin(admin.ModelAdmin):
    list_display = ('groupname',)
    search_fields = ('groupname',)

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('username','email')
    search_fields = ('username',)

#admin.site.register(models.UserType,UserTypeAdmin)
#admin.site.register(models.UserInfo,UserInfoAdmin)
admin.site.register(models.UserGroup,UserGroupAdmin)
admin.site.register(models.Asset,AssetAdmin)