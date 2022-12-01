import json

from django.shortcuts import render
from mainpage.models import Projects, Project_contents, User_Project, Comments
from accounts.models import User

# 프로젝트 생성
def createProject(request):
    data = json.loads(request.body)
    project = Projects(
        project_name = data['project_name']
    )
    project.save()

    project = Projects.objects.get(project_name = data['project_name'])
    user_project = User_Project(
        project_id = project.id,
        email = data['email']
    )
    user_project.save()

    #프로젝트에 topic들 미리 넣어주기(가이드라인)
    # project_contents = Project_contents(
    #     category = ,
    #     topic = ,
    #     state = ,
    #     content = ,
    #     category_index= ,
    #     state_index= ,
    #     image= ,
    #     project_name= ,
    #     project_id= ,
    #     using= 0
    # )
    # project_contents.save()


# 프로필 페이지 정보 및 프로젝트들 정보 전달
def allData(request):




