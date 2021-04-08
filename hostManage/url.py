from django.urls import path,re_path
from hostManage import views
urlpatterns = [
    path('host',views.Host.as_view()),
]
