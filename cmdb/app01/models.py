from django.db import models

# Create your models here.
class UserType(models.Model):
    #加上blank=True:后台对于这个字段就不是必填了
    #typename = models.CharField(verbose_name="用户类型"，max_length=50,blank=True)
    typename = models.CharField(verbose_name="用户类型",max_length=50)
    # 直接排序，每次查询出来的都按name来默认排序
    class Meta:
        verbose_name = '用户类型'  # 改变表在admin中的名字
        ordering = ['typename']
    # 可以在object中看到typename信息
    def __unicode__(self):
        return self.typename       # 显示记录时，用name来区别

class UserInfo(models.Model):
    username = models.CharField(verbose_name="用户名",max_length=50)
    password = models.CharField(verbose_name="用户密码",max_length=50)
    email  = models.EmailField()
    user_type = models.ForeignKey("UserType")

    class Meta:
        verbose_name = '用户信息'
    def __unicode__(self):
        return self.username

class UserGroup(models.Model):
    groupname = models.CharField(verbose_name="用户组",max_length=50)
    user = models.ManyToManyField("UserInfo",verbose_name="用户名")
    class Meta:
        verbose_name = '用户组信息'
    def __unicode__(self):
        return self.groupname

class Asset(models.Model):
    hostname = models.CharField(verbose_name="主机名",max_length=256)
    ip = models.GenericIPAddressField(verbose_name="主机IP",)
    create_date = models.DateTimeField(verbose_name="创建日期",auto_now_add=True)
    update_date = models.DateTimeField(verbose_name="更新日期",auto_now=True)
    user_group = models.ForeignKey("UserGroup")

    class Meta:
        verbose_name = '主机信息'
    def __unicode__(self):
        temp = "Current Object Asset(include:%s %s)" % (self.hostname,self.ip)
        return temp