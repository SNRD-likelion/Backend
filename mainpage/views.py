from django.shortcuts import render
from django.http import JsonResponse
from accounts.models import User
from .models import Projects, Project_contents, User_Project, Comments

import json

# 처음 프로젝트 메인화면 랜딩될 때 전체 데이터 return
def allData(request, project_id):
    try:
        project = Projects.objects.get(pk=project_id)
        PM = []
        Design = []
        Frontend = []
        Backend = []

        # 해당프로젝트의 데이터들을 state별로 그루핑하고 index 오름차순으로 나열
        data_list = Project_contents.objects \
            .filter(project_name=project.project_name) \
            .values('category') \
            .order_by('category_index')

        for data in data_list:
            if data.category == 'PM':
                comment_list = Comments.objects.filter(topic=data.topic, project_name=project.project_name)
                PM.append(
                    {
                        "category": data.category,
                        "topic": data.topic,
                        "category_index": data.category_index,
                        "comment_list": comment_list
                    }
                )
            elif data.category == 'Design':
                comment_list = Comments.objects.filter(topic=data.topic, project_name=project.project_name)
                Design.append(
                    {
                        "category": data.category,
                        "topic": data.topic,
                        "category_index": data.category_index,
                        "comment_list": comment_list
                    }
                )
            elif data.category == 'Frontend':
                comment_list = Comments.objects.filter(topic=data.topic, project_name=project.project_name)
                Frontend.append(
                    {
                        "category": data.category,
                        "topic": data.topic,
                        "category_index": data.category_index,
                        "comment_list": comment_list
                    }
                )
            elif data.category == 'Backend':
                comment_list = Comments.objects.filter(topic=data.topic, project_name=project.project_name)
                Backend.append(
                    {
                        "category": data.category,
                        "topic": data.topic,
                        "category_index": data.category_index,
                        "comment_list": comment_list
                    }
                )

        return JsonResponse({"PM": PM, "Design": Design, "Frontend": Frontend, "Backend": Backend}, status=200)
    except:
        return JsonResponse({"PM": PM, "Design": Design, "Frontend": Frontend, "Backend": Backend}, status=200)

# 카테고리 내에서 순서 변경
def orderChange(request, project_id):
    # 드래그로 토픽의 상태 바뀔 때 db에 반영
    if request.method == 'PUT':
        data = json.loads(request.body)
        PM = data['PM']
        Design = data['Design']
        Frontend = data['Frontend']
        Backend = data['Backend']

        num = 0
        for p in PM:
            row = Project_contents.objects.get(topic = p.topic)
            row.update(category_index = num, category = "PM")
            num = num+1

        num = 0
        for d in Design:
            row = Project_contents.objects.get(topic = d.topic)
            row.update(category_index = num, category="Design")
            num = num + 1

        num = 0
        for f in Frontend:
            row = Project_contents.objects.get(topic = f.topic)
            row.update(category_index = num, category="Frontend")
            num = num + 1

        num = 0
        for b in Backend:
            row = Project_contents.objects.get(topic = b.topic)
            row.update(category_index = num, category="Backend")
            num = num + 1

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
            data_list = Project_contents.objects \
                .filter(project_name=project.project_name) \
                .values('category') \
                .order_by('category_index')

            for data in data_list:
                if data.category == 'PM':
                    comment_list = Comments.objects.filter(topic=data.topic, project_name=project.project_name)
                    PM.append(
                        {
                            "category": data.category,
                            "topic": data.topic,
                            "category_index": data.category_index,
                            "comment_list": comment_list
                        }
                    )
                elif data.category == 'Design':
                    comment_list = Comments.objects.filter(topic=data.topic, project_name=project.project_name)
                    Design.append(
                        {
                            "category": data.category,
                            "topic": data.topic,
                            "category_index": data.category_index,
                            "comment_list": comment_list
                        }
                    )
                elif data.category == 'Frontend':
                    comment_list = Comments.objects.filter(topic=data.topic, project_name=project.project_name)
                    Frontend.append(
                        {
                            "category": data.category,
                            "topic": data.topic,
                            "category_index": data.category_index,
                            "comment_list": comment_list
                        }
                    )
                elif data.category == 'Backend':
                    comment_list = Comments.objects.filter(topic=data.topic, project_name=project.project_name)
                    Backend.append(
                        {
                            "category": data.category,
                            "topic": data.topic,
                            "category_index": data.category_index,
                            "comment_list": comment_list
                        }
                    )

            return JsonResponse({"PM": PM, "Design": Design, "Frontend": Frontend, "Backend": Backend}, status=200)
        except:
            return JsonResponse({"PM": PM, "Design": Design, "Frontend": Frontend, "Backend": Backend}, status=200)