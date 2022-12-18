from django.urls import path
from . import views

urlpatterns = [
    path('<int:user_id>/create', views.createProject), # 프로젝트 생성
    path('<int:user_id>/position', views.editPostion), # 각 프로젝트별 역할 수정
    path('<int:user_id>/information', views.editIntro), #  소개 수정
    path('<int:user_id>/', views.allData), # 처음 프로젝트 띄울 때 프로젝트들 정보넘겨주기
]