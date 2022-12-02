from django.http import JsonResponse
from django.shortcuts import render
from accounts.models import User
from mainpage.models import Projects, Project_contents, User_Project, Comments

import json

# 처음 칸반보드(투두리스트)화면 랜딩될 때 프론트로 데이터 전체 return
def allData(request, project_id):
    try:
        project = Projects.objects.get(pk=project_id)
        Todo = []
        Doing = []
        Review = []
        Done = []


        # 해당프로젝트의 데이터들을 state별로 그루핑하고 index 오름차순으로 나열
        data_list = Project_contents.objects\
            .filter(project_id=project.id)\
            .values('state')\
            .order_by('state_index')
        # commentCounts = Comments.objects.annotate(Count('topic'))
        # comment_list = Comments.objects\
        #     .filter(project_name=project.project_name)\
        #     .values('topic')
        
        for data in data_list:
            if data.state == 'todo':
                comment_list = Comments.objects.filter(topic = data.topic, project_id = project.id)
                Todo.append(
                    {
                        "state": data.state,
                        "category": data.category,
                        "topic": data.topic,
                        "state_index": data.state_index,
                        "comment_list": comment_list
                    }
                )
            elif data.state == 'doing':
                comment_list = Comments.objects.filter(topic=data.topic, project_id = project.id)
                Doing.append(
                    {
                        "state": data.state,
                        "category": data.category,
                        "topic": data.topic,
                        "state_index": data.state_index,
                        "comment_list": comment_list
                    }
                )
            elif data.state == 'review':
                comment_list = Comments.objects.filter(topic=data.topic, project_id = project.id)
                Review.append(
                    {
                        "state": data.state,
                        "category": data.category,
                        "topic": data.topic,
                        "state_index": data.state_index,
                        "comment_list": comment_list
                    }
                )
            elif data.state == 'done':
                comment_list = Comments.objects.filter(topic=data.topic, project_id = project.id)
                Done.append(
                    {
                        "state": data.state,
                        "category": data.category,
                        "topic": data.topic,
                        "state_index": data.state_index,
                        "comment_list": comment_list
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

        num = 0
        for t in todo:
            row = Project_contents.objects.get(pk = t.id)
            row.update(state_index = num, state = "todo")
            num = num+1

        num = 0
        for d in doing:
            row = Project_contents.objects.get(pk = d.id)
            row.update(state_index = num, state="doing")
            num = num + 1

        num = 0
        for r in review:
            row = Project_contents.objects.get(pk = r.id)
            row.update(state_index = num, state="review")
            num = num + 1

        num = 0
        for d in done:
            row = Project_contents.objects.get(pk = d.id)
            row.update(state_index = num, state="done")
            num = num + 1

    # 드래그로 db반영이 끝난 이후 5초이후에 프론트에서 refresh할 때 다시 데이터 쏴줌
    # 근데 이럴거면 위에 allData랑 아예 똑같긴해서 이건 프론트랑 협의 필요
    if request.method == 'GET':
        try:
            project = Projects.objects.get(pk=project_id)
            Todo = []
            Doing = []
            Review = []
            Done = []

            # 해당프로젝트의 데이터들을 state별로 그루핑하고 index 오름차순으로 나열
            data_list = Project_contents.objects \
                .filter(project_id=project.id) \
                .values('state') \
                .order_by('state_index')
            # commentCounts = Comments.objects.annotate(Count('topic'))
            # comment_list = Comments.objects\
            #     .filter(project_name=project.project_name)\
            #     .values('topic')

            for data in data_list:
                if data.state == 'todo':
                    comment_list = Comments.objects.filter(topic=data.topic, project_id=project.id)
                    Todo.append(
                        {
                            "state": data.state,
                            "category": data.category,
                            "topic": data.topic,
                            "state_index": data.state_index,
                            "comment_list": comment_list
                        }
                    )
                elif data.state == 'doing':
                    comment_list = Comments.objects.filter(topic=data.topic, project_id=project.id)
                    Doing.append(
                        {
                            "state": data.state,
                            "category": data.category,
                            "topic": data.topic,
                            "state_index": data.state_index,
                            "comment_list": comment_list
                        }
                    )
                elif data.state == 'review':
                    comment_list = Comments.objects.filter(topic=data.topic, project_id=project.id)
                    Review.append(
                        {
                            "state": data.state,
                            "category": data.category,
                            "topic": data.topic,
                            "state_index": data.state_index,
                            "comment_list": comment_list
                        }
                    )
                elif data.state == 'done':
                    comment_list = Comments.objects.filter(topic=data.topic, project_id=project.id)
                    Done.append(
                        {
                            "state": data.state,
                            "category": data.category,
                            "topic": data.topic,
                            "state_index": data.state_index,
                            "comment_list": comment_list
                        }
                    )

            return JsonResponse({"todo": Todo, "doing": Doing, "review": Review, "done": Done}, status=200)
        except:
            return JsonResponse({"todo": Todo, "doing": Doing, "review": Review, "done": Done}, status=200)
        


