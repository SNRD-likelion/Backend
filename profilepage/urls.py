from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.createProject), # 프로젝트 생성
]