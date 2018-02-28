from django.db import models

# Create your models here.
class HostInfo(models.Model):
    hostname = models.CharField(verbose_name="主机名",max_length=256)
    ip = models.GenericIPAddressField(verbose_name="主机IP",max_length=50)
    class Meta:
        verbose_name = '主机信息'
    def __unicode__(self):
        return self.ip

class  MysqlInfo(models.Model):
    mysql_port = models.IntegerField(verbose_name="端口")
    mysql_user = models.CharField(verbose_name="用户",max_length=32)
    mysql_passwd = models.CharField(verbose_name="密码",max_length=32)
    mysql_socket = models.CharField(verbose_name="Socket",max_length=32)
    mysql_remark = models.CharField(verbose_name="备注",max_length=32)
    mysql_host = models.ForeignKey("HostInfo")
    class Meta:
        verbose_name = 'MySQL信息'
    def __unicode__(self):
        temp = "Current Object Asset(include:%s %s)" % (self.mysqlport,self.mysql_host)
        return temp
class DatabaseInfo(models.Model):
    database_name = models.CharField(verbose_name="数据库名",max_length=32)
    database_mysql = models.ForeignKey("MysqlInfo")
    class Meta:
        verbose_name = '数据库信息'
    def __unicode__(self):
        return self.db_name


class DatabaseSize(models.Model):
    database_size = models.CharField(verbose_name="数据库大小[Mb]",max_length=32)
    database_info = models.ForeignKey("DatabaseInfo")
#    create_date = models.DateTimeField(verbose_name="创建日期",auto_now_add=True)
#    update_date = models.DateTimeField(verbose_name="更新日期",auto_now=True)
    create_date = models.DateField(verbose_name="创建日期",auto_now_add=True)
    update_date = models.DateField(verbose_name="更新日期",auto_now=True)
    class Meta:
        verbose_name = '数据库大小'
    def __unicode__(self):
        return self.db_name

class TableInfo(models.Model):
    table_name = models.CharField(verbose_name="数据库名",max_length=32)
#    first_attr =  models.CharField(verbose_name="字段名",max_length=32)
    table_database = models.ForeignKey("DatabaseInfo")
    table_mysql = models.ForeignKey("MysqlInfo")
    table_host = models.ForeignKey("HostInfo")
    class Meta:
        verbose_name = '表信息'
    def __unicode__(self):
        return self.db_name

class TableCount(models.Model):
    table_count = models.IntegerField(verbose_name="表记录数")
    table_info = models.ForeignKey("TableInfo")
#    create_date = models.DateTimeField(verbose_name="创建日期",auto_now_add=True)
#    update_date = models.DateTimeField(verbose_name="更新日期",auto_now=True)
    create_date = models.DateField(verbose_name="创建日期",auto_now_add=True)
    update_date = models.DateField(verbose_name="更新日期",auto_now=True)
    class Meta:
        verbose_name = '表记录数'
    def __unicode__(self):
        return self.table_size
