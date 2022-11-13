from django.urls import path
from . import views

urlpatterns = [
    path('<int:project_id>/', views.allData), # GET 칸반보드 페이지 처음 랜딩될 때 데이터전체 전달

]
