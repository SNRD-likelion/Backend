from django.shortcuts import render
from django.http import JsonResponse
from accounts.models import User
from .models import Projects, Project_contents, User_Project, Comments

# Create your views here.
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

        return JsonResponse({"todo": PM, "doing": Design, "review": Frontend, "done": Backend}, status=200)
    except:
        return JsonResponse({"todo": PM, "doing": Design, "review": Frontend, "done": Backend}, status=200)
