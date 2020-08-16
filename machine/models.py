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

