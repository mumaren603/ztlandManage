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
    # user_rel_auth = models.ForeignKey('Auth',to_field='auth_id',on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_now_add=True)
    uptime = models.DateTimeField(auto_now=True)
    auth_rel = models.ManyToManyField("Auth")

# 权限表（主要针对页面环境信息，主机信息模块新增，编辑，删除权限）
class Auth(models.Model):
    auth_id = models.AutoField(primary_key=True,default=10000)
    authname = models.CharField(max_length=32,null=False)
    authcode = models.CharField(max_length=32,null=False)
    # r = models.ManyToManyField("UserInfo")

#环境信息主表
class EnvInfo(models.Model):
    m_id = models.AutoField(primary_key=True)
    env_name = models.CharField(max_length=32,db_index=True,null=False)
    #env_node = models.CharField(max_length=32,unique=True)
    frontIP = models.GenericIPAddressField(protocol='ipv4')
    backIP = models.GenericIPAddressField(protocol='ipv4')
    dbIP = models.GenericIPAddressField(protocol='ipv4')
    status = models.CharField(max_length=32)                                  # 在用，废弃，挂起

#环境信息子表
class EnvDetailInfo(models.Model):
    s_id = models.AutoField(primary_key=True)
    service_chinese_name = models.CharField(max_length=32,db_index=True,null=False)
    service_name = models.CharField(max_length=32,db_index=True,null=False)
    service_host = models.GenericIPAddressField(protocol='ipv4')
    service_port = models.IntegerField()
    service_deploy_path = models.CharField(max_length=200)
    service_url = models.CharField(max_length=50)
    service_model = models.CharField(max_length=32,null=False)  # 前端 后端 微服务
    env_sub_node = models.ForeignKey('EnvInfo',to_field='m_id',on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_now_add=True)
    uptime = models.DateTimeField(auto_now=True)

#数据库信息表
class DbInfo(models.Model):
    db_id = models.AutoField(primary_key=True)
    ip = models.GenericIPAddressField(protocol='ipv4',db_index=True)
    port = models.IntegerField()
    sid = models.CharField(max_length=32,null=False)    #实例
    user = models.CharField(max_length=32,null=False)
    password = models.CharField(max_length=32,null=False)
    name = models.CharField (max_length=32,null=False)  #登记结果库
    db_node = models.ForeignKey('EnvInfo', to_field='m_id', on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_now_add=True)
    uptime = models.DateTimeField(auto_now=True)


#服务器实体机信息
class  ServerInfo(models.Model):
    intranetIP = models.GenericIPAddressField(protocol='ipv4',null=False)
    extrantIP = models.GenericIPAddressField(protocol='ipv4',null=True)
    serverType = models.CharField(max_length=10,null=False)
    serverPurpose = models.CharField(max_length=32)
    serverAccount = models.CharField(max_length=32,null=False)
    serverPassword = models.CharField(max_length=32, null=False)
    serverOs = models.CharField(max_length=32,null=False)
    originServer = models.CharField(max_length=32, null=True)
    ctime = models.DateTimeField(auto_now_add=True)
    uptime = models.DateTimeField(auto_now=True)

