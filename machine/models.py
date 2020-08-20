from django.db import models

# Create your models here.
#  ----- 项目初始化脚本 ------
# 用户信息表
class UserInfo(models.Model):
    username = models.CharField(max_length=32,null=False)
    password = models.CharField(max_length=32,null=False)
    email = models.EmailField()
    gender = models.CharField(max_length=6,null=True)
    telephoneNum = models.IntegerField(null=True)


#环境信息表
class EnvInfo(models.Model):
    service_chinese_name = models.CharField(max_length=32,null=False)
    service_name = models.CharField(max_length=32,null=False)
    service_host = models.GenericIPAddressField()
    service_port = models.IntegerField()
    service_deploy_path = models.CharField(max_length=200)
    service_url = models.CharField(max_length=50)
    service_model = models.CharField(max_length=32,null=False)
    env_model = models.CharField(max_length=32, null=False)
    ctime = models.DateTimeField(auto_now_add=True)
    uptime = models.DateTimeField(auto_now=True)

#数据库信息表
class DbInfo(models.Model):
    db_id = models.AutoField(primary_key=True)
    ip = models.GenericIPAddressField()
    ip_vpn = models.GenericIPAddressField()
    port = models.IntegerField()
    sid = models.CharField(max_length=32,null=False)
    user = models.CharField(max_length=32,null=False)
    password = models.CharField(max_length=32,null=False)
    name = models.CharField(max_length=32,null=False)
    db_model = models.CharField(max_length=32,null=False)
    ctime = models.DateTimeField(auto_now_add=True)
    uptime = models.DateTimeField(auto_now=True)
