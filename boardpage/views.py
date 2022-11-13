from django.http import JsonResponse
from django.shortcuts import render
from accounts.models import User
from mainpage.models import Projects, Project_contents, User_Project, Comments
from django.db.models import Count

# Create your views here.
def allData(request, project_id):
    try:
        project = Projects.objects.get(pk=project_id)
        Todo = []
        Doing = []
        Review = []
        Complete = []
        Comments = []
        data_list= Project_contents.objects.filter(project_name=project.project_name)
        # commentCounts = Comments.objects.annotate(Count('topic'))

        for data in data_list:
            if data.state == "해야할 일":
                Todo.append(
                    {
                        "state": data.state,
                        "category": data.category,
                        "topic": data.topic,
                    }
                )
            elif data.state == "진행 중":
                Doing.append(
                    {
                        "state": data.state,
                        "category": data.category,
                        "topic": data.topic,
                    }
                )
            elif data.state == "리뷰 중":
                Review.append(
                    {
                        "state": data.state,
                        "category": data.category,
                        "topic": data.topic,
                    }
                )
            elif data.state == "완료":
                Complete.append(
                    {
                        "state": data.state,
                        "category": data.category,
                        "topic": data.topic,
                    }
                )


        return JsonResponse({"해야할 일": Todo, "진행 중": Doing, "리뷰 중": Review, "완료": Complete}, status=200)
    except:
        return JsonResponse({"해야할 일": Todo, "진행 중": Doing, "리뷰 중": Review, "완료": Complete}, status=200)

# def stateChange(request):
#     try:


