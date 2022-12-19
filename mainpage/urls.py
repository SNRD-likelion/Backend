from django.urls import path
from . import views

urlpatterns = [
    path('<int:project_id>/', views.allData), # GET 메인페이지(원페이저) 처음 랜딩될 때 데이터전체 전달
    path('<int:project_id>/change', views.orderChange), # 드래그해서 순서바꾸기
    path('<int:project_id>/comment', views.createComment), # 댓글작성
    # path('<int:project_id>/addMember', views.addMember), # 멤버추가(초대)
    path('<int:project_id>/editStart', views.editStart), #토픽내용수정 시작, using=0이면 수정가능, 1이면 누군가 수정중이라 불가
    path('<int:project_id>/<int:topic_id>/editTopicContents', views.editTopicContents), #토픽내용수정
    path('<int:project_id>/<int:topic_id>/addTopic', views.addTopic), #토픽추가
]