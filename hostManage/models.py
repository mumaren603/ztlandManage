from django.db import models

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

