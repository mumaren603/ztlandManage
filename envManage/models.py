from django.db import models

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

