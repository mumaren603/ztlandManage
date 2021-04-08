from django.contrib import admin
from django.urls import path,re_path
from dataManage import views

urlpatterns = [
    path('data', views.Data.as_view()),
]

