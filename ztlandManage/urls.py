"""ztlandManage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from machine import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login),
    path('logout/',views.logout),
    path('index', views.index),
    # re_path('home$', views.home),
    re_path('env$', views.env),
    re_path('env/detail-(?P<nid>\d+)', views.envDetail),
    re_path('env/delEnv-(?P<nid>\d+)', views.envDel),
    re_path('env/delDb-(?P<nid>\d+)', views.dbDel),
    path('env/query',views.envQuery),
    path('env/addEnv',views.envAdd),
    path('env/editEnvDetail', views.envDetailedit.as_view()),
    path('env/editDbDetail', views.dbDetailedit.as_view()),
    path('env/addEnvDetail',views.envDetailAdd),
    path('env/addDbDetail',views.dbDetailAdd),
    path('host/',views.Host.as_view()),
    path('data/', views.Data.as_view()),
]

