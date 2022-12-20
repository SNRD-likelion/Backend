from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from accounts.models import User
from .models import Projects, Project_content, User_Project, Comments

import json

# 처음 프로젝트 메인화면 랜딩될 때 전체 데이터 return
def allData(request, project_id):
        project = Projects.objects.get(pk=project_id)
        PM = []
        Design = []
        Frontend = []
        Backend = []

        # 해당프로젝트의 데이터들을 state별로 그루핑하고 index 오름차순으로 나열
        data_list = Project_content.objects \
            .filter(project_id=project_id) \
            .order_by('category_index')

        # .values('category') \

        for data in data_list:

            if data.category == 'PM':
                # comment_list = Comments.objects.filter(topic=data.topic, project_id=project_id)
                comment_list = []

                PM.append(
                    {
                        "id": data.id,
                        "category": data.category,
                        "topic": data.topic,
                        "category_index": data.category_index,
                        "comment_list": comment_list,
                        "contents": data.contents
                    }
                )
            elif data.category == 'Design':
                # comment_list = Comments.objects.filter(topic=data.topic, project_id=project_id)
                comment_list = []
                Design.append(
                    {
                        "id": data.id,
                        "category": data.category,
                        "topic": data.topic,
                        "category_index": data.category_index,
                        "comment_list": comment_list,
                        "contents": data.contents
                    }
                )
            elif data.category == 'Frontend':
                # comment_list = Comments.objects.filter(topic=data.topic, project_id=project_id)
                comment_list = []
                Frontend.append(
                    {
                        "id": data.id,
                        "category": data.category,
                        "topic": data.topic,
                        "category_index": data.category_index,
                        "comment_list": comment_list,
                        "contents": data.contents
                    }
                )
            elif data.category == 'Backend':
                # comment_list = Comments.objects.filter(topic=data.topic, project_id=project_id)
                comment_list = []
                Backend.append(
                    {
                        "id": data.id,
                        "category": data.category,
                        "topic": data.topic,
                        "category_index": data.category_index,
                        "comment_list": comment_list,
                        "contents": data.contents
                    }
                )

        return JsonResponse({"PM": PM, "Design": Design, "Frontend": Frontend, "Backend": Backend}, status=200)

# 카테고리 내에서 순서 변경
def orderChange(request, project_id):
    # 드래그로 토픽의 상태 바뀔 때 db에 반영
    if request.method == 'POST':
        data = json.loads(request.body)
        PM = data['PM']
        Design = data['Design']
        Frontend = data['Frontend']
        Backend = data['Backend']

        num = 0
        for p in PM:
            # topic = p.topic, project_id = project_id, category = "PM"
            row = Project_content.objects.get(pk = p['id'])
            # row.update(category_index = num, category = "PM")
            row.category_index = num
            row.category = "PM"
            row.save()
            num = num+1


        num = 0
        for d in Design:
            # topic = d.topic, project_id = project_id, category = "Design"
            row = Project_content.objects.get(pk = d['id'])
            # row.update(category_index = num, category="Design")
            row.category_index = num
            row.category = "Design"
            row.save()
            num = num + 1


        num = 0
        for f in Frontend:
            # topic = f.topic, project_id = project_id, category = "Frontend"
            row = Project_content.objects.get(pk = f['id'])
            # row.update(category_index = num, category="Frontend")
            row.category_index = num
            row.category = "Frontend"
            row.save()
            num = num + 1

        num = 0
        for b in Backend:
            # topic = b.topic, project_id = project_id, category = "Backend"
            row = Project_content.objects.get(pk = b['id'])
            # row.update(category_index = num, category="Backend")
            row.category_index = num
            row.category = "Backend"
            row.save()
            num = num + 1

        return HttpResponse(status=200)

    # 드래그로 db반영이 끝난 이후 5초이후에 프론트에서 refresh할 때 다시 데이터 쏴줌
    # 근데 이럴거면 위에 allData랑 아예 똑같긴해서 이건 프론트랑 협의 필요
    if request.method == 'GET':
        try:
            project = Projects.objects.get(pk=project_id)
            PM = []
            Design = []
            Frontend = []
            Backend = []

            # 해당프로젝트의 데이터들을 state별로 그루핑하고 index 오름차순으로 나열
            data_list = Project_content.objects \
                .filter(project_id=project.id) \
                .values('category') \
                .order_by('category_index')

            for data in data_list:
                if data.category == 'PM':
                    comment_list = Comments.objects.filter(topic=data.topic, project_id=project.id)
                    PM.append(
                        {
                            "id": data.id,
                            "category": data.category,
                            "topic": data.topic,
                            "category_index": data.category_index,
                            "comment_list": comment_list
                        }
                    )
                elif data.category == 'Design':
                    comment_list = Comments.objects.filter(topic=data.topic, project_id=project.id)
                    Design.append(
                        {
                            "id": data.id,
                            "category": data.category,
                            "topic": data.topic,
                            "category_index": data.category_index,
                            "comment_list": comment_list
                        }
                    )
                elif data.category == 'Frontend':
                    comment_list = Comments.objects.filter(topic=data.topic, project_id=project.id)
                    Frontend.append(
                        {
                            "id": data.id,
                            "category": data.category,
                            "topic": data.topic,
                            "category_index": data.category_index,
                            "comment_list": comment_list
                        }
                    )
                elif data.category == 'Backend':
                    comment_list = Comments.objects.filter(topic=data.topic, project_id=project.id)
                    Backend.append(
                        {
                            "id": data.id,
                            "category": data.category,
                            "topic": data.topic,
                            "category_index": data.category_index,
                            "comment_list": comment_list
                        }
                    )

            return JsonResponse({"PM": PM, "Design": Design, "Frontend": Frontend, "Backend": Backend}, status=200)
        except:
            return JsonResponse({"PM": PM, "Design": Design, "Frontend": Frontend, "Backend": Backend}, status=200)

# 댓글작성
def createComment(request, project_id):
    data = json.loads(request.body)
    forState = Project_content.objects.get(project_id=project_id, category=data['category'], topic=data['topic'])
    comment = Comments(
        user = data['email'],
        contents = data['contents'],
        project_id = project_id,
        topic = data['topic'],
        state = forState.state,
        category = data['category']
    )
    comment.save()

# 프로젝트에 멤버추가(초대)
# def addMember(request, project_id):
#     data = json.loads(request.body)
#     user_project = User_Project(
#         user = data['email'],
#         project_id = project_id
#     )
#     user_project.save()

#프로젝트 정보수정
def editProjectInfo(request, project_id):
    data = json.loads(request.body)
    project = Projects.objects.get(pk=project_id)
    project.update(project_name=data['title'], duration=data['duration'], slogan=data['slogan'])
    teammates = data['teammates']

    for t in teammates:
        user_project= User_Project(
            project_id=project_id,
            email=t
        )
        user_project.save()


# 토픽수정시작할 때 post쏴주면 수정중인 사람 있는지 없는지 파악가능
def editStart(request, project_id):
    data = json.loads(request.body)
    project_contents = Project_content.objects.get(pk=data['id'])

    if project_contents.using == 1:
        return JsonResponse({"message": "누군가 수정 중입니다."}, status=200)
    else:
        project_contents.using = 1
        project_contents.save()

def editTopicTitle(request, project_id, topic_id):
    data = json.loads(request.body)
    project_contents = Project_content.objects.get(pk=data['id'])
    project_contents.topic = data['topic']
    project_contents.save()

    return HttpResponse(status=200)

# 토픽 내용수정
def editTopicContents(request, project_id, topic_id):
    data = json.loads(request.body)
    project_contents = Project_content.objects.get(pk=data['id'])
    print(data['contents'])
    # project_contents.update(contents=data['contents'], using=0)
    project_contents.contents=data['contents']
    project_contents.using = 0
    project_contents.save()

    return HttpResponse(status=200)

# 토픽 새로추가
def addTopic(request, project_id, topic_id):
    data = json.loads(request.body)

    forProjectName= Projects.objects.get(project_id=project_id)
    forCountCategory= Project_content.objects.filter(project_id=project_id, category=data['category'])
    categoryCount = forCountCategory.count()
    forCountState = Project_content.objects.filter(project_id=project_id, state='todo')
    stateCount = forCountState.count()

    project_contents = Project_content(
        category=data['category'],
        topic=data['topic'],
        state='todo',
        content='',
        category_index=categoryCount,
        state_index=stateCount,
        project_name=forProjectName.project_name,
        project_id=project_id,
        using=0
    )
    project_contents.save()