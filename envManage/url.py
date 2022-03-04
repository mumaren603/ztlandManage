from django.contrib import admin
from django.urls import path,re_path
from envManage import views

urlpatterns = [
    re_path('env$', views.env),
    path('env/query', views.envQuery),
    path('env/add', views.envAdd),
    path('env/edit', views.envEdit),
    path('env/del', views.envDel),
    path('env/exportEnv', views.envExport),
    path('env/exportDb', views.dbExport),
    # re_path('env/detail-(?P<nid>\d+)', views.envDetail),
    re_path('env/detail-(?P<nid>\d+)-(?P<uid>\d+)', views.envDetail.as_view()),
    path('env/detail/edit', views.envDetailedit.as_view()),
    path('db/detail/edit', views.dbDetailedit.as_view()),
    path('env/detail/del', views.envDetaildel.as_view()),
    path('env/detail/add', views.envDetailAdd),
    path('db/detail/add', views.dbDetailAdd),
]

