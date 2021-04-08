from django.contrib import admin
from django.urls import path,re_path
from envManage import views

urlpatterns = [
    re_path('env$', views.env),
    re_path('env/detail-(?P<nid>\d+)', views.envDetail),
    re_path('env/delEnv-(?P<nid>\d+)', views.envDel),
    re_path('env/delDb-(?P<nid>\d+)', views.dbDel),
    path('env/query', views.envQuery),
    path('env/addEnv', views.envAdd),
    path('env/editEnvDetail', views.envDetailedit.as_view()),
    path('env/editDbDetail', views.dbDetailedit.as_view()),
    path('env/addEnvDetail', views.envDetailAdd),
    path('env/addDbDetail', views.dbDetailAdd),
]

