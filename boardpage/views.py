from django.http import JsonResponse
from django.shortcuts import render
from accounts.models import User
from mainpage.models import Projects, Project_contents, User_Project, Comments
from django.db.models import Count
import json

# 처음 칸반보드(투두리스트)화면 랜딩될 때 프론트로 데이터 전체 return
def allData(request, project_id):
    try:
        project = Projects.objects.get(pk=project_id)
        Todo = []
        Doing = []
        Review = []
        Done = []
        Comments = []
        data_list= Project_contents.objects.filter(project_name=project.project_name)
        # commentCounts = Comments.objects.annotate(Count('topic'))

        for data in data_list:
            if data.state == "todo":
                Todo.append(
                    {
                        "state": data.state,
                        "category": data.category,
                        "topic": data.topic,
                        "state_index": data.state_index
                    }
                )
            elif data.state == "doing":
                Doing.append(
                    {
                        "state": data.state,
                        "category": data.category,
                        "topic": data.topic,
                        "state_index": data.state_index
                    }
                )
            elif data.state == "review":
                Review.append(
                    {
                        "state": data.state,
                        "category": data.category,
                        "topic": data.topic,
                        "state_index": data.state_index
                    }
                )
            elif data.state == "done":
                Done.append(
                    {
                        "state": data.state,
                        "category": data.category,
                        "topic": data.topic,
                        "state_index": data.state_index
                    }
                )


        return JsonResponse({"todo": Todo, "doing": Doing, "review": Review, "done": Done}, status=200)
    except:
        return JsonResponse({"todo": Todo, "doing": Doing, "review": Review, "done": Done}, status=200)

def stateChange(request, project_id):
    # 드래그로 토픽의 상태 바뀔 때 db에 반영
    if request.method == 'PUT':
        data = json.loads(request.body)
        todo = data['todo']
        doing = data['doing']
        review = data['review']
        done = data['done']

        for t in todo:
            num = t.state_index
            row = Project_contents.objects.get(topic = t.topic)
            row.update(state_index = num)

        for d in doing:
            num = d.state_index
            row = Project_contents.objects.get(topic = d.topic)
            row.update(state_index = num)

        for r in review:
            num = r.state_index
            row = Project_contents.objects.get(topic = r.topic)
            row.update(state_index = num)

        for d in done:
            num = d.state_index
            row = Project_contents.objects.get(topic = d.topic)
            row.update(state_index = num)

    # 드래그로 db반영이 끝난 이후 5초이후에 프론트에서 refresh할 때 다시 데이터 쏴줌
    # 근데 이럴거면 위에 allData랑 아예 똑같긴해서 이건 프론트랑 협의 필요
    if request.method == 'GET':
        try:
            project = Projects.objects.get(pk=project_id)
            Todo = []
            Doing = []
            Review = []
            Done = []
            Comments = []
            data_list = Project_contents.objects.filter(project_name=project.project_name)
            # commentCounts = Comments.objects.annotate(Count('topic'))

            for data in data_list:
                if data.state == "todo":
                    Todo.append(
                        {
                            "state": data.state,
                            "category": data.category,
                            "topic": data.topic,
                            "state_index": data.state_index
                        }
                    )
                elif data.state == "doing":
                    Doing.append(
                        {
                            "state": data.state,
                            "category": data.category,
                            "topic": data.topic,
                            "state_index": data.state_index
                        }
                    )
                elif data.state == "review":
                    Review.append(
                        {
                            "state": data.state,
                            "category": data.category,
                            "topic": data.topic,
                            "state_index": data.state_index
                        }
                    )
                elif data.state == "done":
                    Done.append(
                        {
                            "state": data.state,
                            "category": data.category,
                            "topic": data.topic,
                            "state_index": data.state_index
                        }
                    )

            return JsonResponse({"todo": Todo, "doing": Doing, "review": Review, "done": Done}, status=200)
        except:
            return JsonResponse({"todo": Todo, "doing": Doing, "review": Review, "done": Done}, status=200)
        


