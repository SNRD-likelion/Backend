import json

from django.http import JsonResponse
from django.shortcuts import render
from mainpage.models import Projects, Project_contents, User_Project, Comments
from accounts.models import User

# 프로젝트 생성
def createProject(request):
    data = json.loads(request.body)
    project = Projects(
        project_name = data['project_name'],
        slogan= data['slogan'],
        duration= data['duration']
    )
    project.save()

    project = Projects.objects.get(project_name=data['project_name'], slogan=data['slogan'])
    teammates = data['teammates']
    for t in teammates:
        user_project= User_Project(
            project_id=project.id,
            email=t
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

    PM = ['아이디어', '타겟과 목적', '목표가 아닌 것', '시장조사', '서비스의 배경', '유사한 서비스 탐구', '비즈니스 모델']
    Design = ['스케치', '무드보드', '와이어프레임', '프로토타입']
    Frontend = ['개발도구 선정', '개발환경세팅', '페이지별 진행상황', '메인화면', '통신 및 테스트', '배포']
    Backend = ['세부기능 구성', '데이터모델링', '개발도구 선정', '개발환경세팅', 'DB구축', '기능구현', '피드백 및 수정', '배포', '통신 및 테스트']


    #PM에 미리 넣어주기
    i = 0
    j = 0
    while i < 7:
        project_contents = Project_contents(
            category= 'PM',
            topic=PM[i],
            state='todo',
            content='',
            category_index=i,
            state_index=j,
            project_name=data['project_name'],
            project_id=project.id,
            using=0
        )
        project_contents.save()
        i=i+1
        j = j+1


    # PM에 미리 넣어주기
    i = 0
    while i < 4:
        project_contents = Project_contents(
            category='Design',
            topic=Design[i],
            state='todo',
            content='',
            category_index=i,
            state_index=i,
            project_name=data['project_name'],
            project_id = project.id,
            using=0
        )
        project_contents.save()
        i = i + 1
        j = j + 1


    # PM에 미리 넣어주기
    i = 0
    while i < 6:
        project_contents = Project_contents(
            category='Frontend',
            topic=Frontend[i],
            state='todo',
            content='',
            category_index=i,
            state_index=i,
            project_name=data['project_name'],
            project_id=project.id,
            using=0
        )
        project_contents.save()
        i = i + 1
        j = j + 1


    # PM에 미리 넣어주기
    i = 0
    while i < 9:
        project_contents = Project_contents(
            category='Backend',
            topic=Backend[i],
            state='todo',
            content='',
            category_index=i,
            state_index=i,
            project_name=data['project_name'],
            project_id=project.id,
            using=0
        )
        project_contents.save()
        i = i + 1
        j = j + 1





# 프로필 페이지 정보 및 프로젝트들 정보 전달
def allData(request, email):
    try:
        data_list = User_Project.objects.filter(email=email)
        project_list = []
        user = User.objects.get(email=email)
        user_inform = {
            'email': user.email,
            'name': user.name,
            'information': user.information
        }

        for d in data_list:
            a = Projects.objects.get(pk=d.project_id)
            user_project = User_Project.objects.filter(project_id=d.project_id)
            userlist=[]
            for u in user_project:
                userlist.append(u.email)
            project_list.append(
                {
                    'id': d.project_id,
                    'title': a.project_name,
                    'teammates': userlist,
                    'duration' : a.duration,
                    'introduction' : a.slogan
                }
            )


        return JsonResponse({"project_list": project_list, "user": user_inform}, status=200)
    except:
        return JsonResponse({"project_list": ""}, status=200)

def editPostion(request, email):
    data = json.loads(request.body)
    user_project = User_Project.objects.get(email=email, project_id=data['project_id'])
    user_project.update(position=data['position'])

def editIntro(request, email):
    data = json.loads(request.body)
    user = User.objects.get(email=email)
    user.update(information=data['information'], name=data['name'])





