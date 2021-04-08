from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path(r'common/', include("commonManage.url")),
    path(r'envManage/', include("envManage.url")),
    path(r'hostManage/',include("hostManage.url")),
    path(r'dataManage/',include("dataManage.url")),
]



