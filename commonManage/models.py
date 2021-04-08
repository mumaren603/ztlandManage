from django.db import models

# Create your models here.
#  ----- 项目初始化脚本 ------
# 用户信息表
class UserInfo(models.Model):
    username = models.CharField(max_length=32,null=False)
    password = models.CharField(max_length=32,null=False)
    email = models.EmailField(null=True)
    gender = models.CharField(max_length=6,null=True)
    telephoneNum = models.IntegerField(null=True)
    ctime = models.DateTimeField(auto_now_add=True)
    uptime = models.DateTimeField(auto_now=True)
    auth_rel = models.ManyToManyField("Auth")      #多对多

# 权限表（主要针对页面环境信息，主机信息模块新增，编辑，删除权限）
class Auth(models.Model):
    auth_id = models.AutoField(primary_key=True,default=10000)
    authname = models.CharField(max_length=32,null=False)
    authcode = models.CharField(max_length=32,null=False)




