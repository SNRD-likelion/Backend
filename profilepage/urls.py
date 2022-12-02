from django.urls import path
from . import views

urlpatterns = [
    path('<email>/create/', views.createProject), # 프로젝트 생성
    path('<email>/', views.allData), # 처음 프로젝트 띄울 때 프로젝트들 정보넘겨주기
]