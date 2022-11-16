from django.urls import path
from . import views

urlpatterns = [
    path('<int:project_id>/', views.allData), # GET 메인페이지(원페이저) 처음 랜딩될 때 데이터전체 전달
    # path('<int:project_id>/change', views.change),
]