from django.contrib import admin
from django.urls import path,re_path
from commonManage import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login',views.login),
    path('logout',views.logout),
    path('index', views.index),
    # path('page_list', views.page_list),
]

