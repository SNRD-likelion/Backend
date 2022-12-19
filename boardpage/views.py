from django.http import JsonResponse
from django.shortcuts import render
from accounts.models import User
from mainpage.models import Projects, Project_content, User_Project, Comments

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
        data_list = Project_content.objects\
            .filter(project_id=project.id)\
            .order_by('state_index')
        # .values('state')\
        # commentCounts = Comments.objects.annotate(Count('topic'))
        # comment_list = Comments.objects\
        #     .filter(project_name=project.project_name)\
        #     .values('topic')
        
        for data in data_list:
            if data.state == 'todo':
                # comment_list = Comments.objects.filter(topic=data.topic, project_id=project_id)
                comment_list = []
                Todo.append(
                    {
                        "id": data.id,
                        "state": data.state,
                        "category": data.category,
                        "topic": data.topic,
                        "state_index": data.state_index,
                        "comment_list": comment_list
                    }
                )
            elif data.state == 'doing':
                # comment_list = Comments.objects.filter(topic=data.topic, project_id=project_id)
                comment_list = []
                Doing.append(
                    {
                        "id": data.id,
                        "state": data.state,
                        "category": data.category,
                        "topic": data.topic,
                        "state_index": data.state_index,
                        "comment_list": comment_list
                    }
                )
            elif data.state == 'review':
                # comment_list = Comments.objects.filter(topic=data.topic, project_id=project_id)
                comment_list = []
                Review.append(
                    {
                        "id": data.id,
                        "state": data.state,
                        "category": data.category,
                        "topic": data.topic,
                        "state_index": data.state_index,
                        "comment_list": comment_list
                    }
                )
            elif data.state == 'done':
                # comment_list = Comments.objects.filter(topic=data.topic, project_id=project_id)
                comment_list = []
                Done.append(
                    {
                        "id": data.id,
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
    if request.method == 'POST':
        data = json.loads(request.body)
        todo = data['todo']
        doing = data['doing']
        review = data['review']
        done = data['done']

        num = 0
        for t in todo:
            row = Project_content.objects.get(pk = t.id)
            row.update(state_index = num, state = "todo")
            num = num+1

        num = 0
        for d in doing:
            row = Project_content.objects.get(pk = d.id)
            row.update(state_index = num, state="doing")
            num = num + 1

        num = 0
        for r in review:
            row = Project_content.objects.get(pk = r.id)
            row.update(state_index = num, state="review")
            num = num + 1

        num = 0
        for d in done:
            row = Project_content.objects.get(pk = d.id)
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
            data_list = Project_content.objects \
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
                            "id": data.id,
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
                            "id": data.id,
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
                            "id": data.id,
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
                            "id": data.id,
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
        
def addTopic(request, project_id):
    data = json.loads(request.body)

    forProjectName= Projects.objects.get(project_id=project_id)
    forCountCategory= Project_content.objects.filter(project_id=project_id, category=data['category'])
    categoryCount = forCountCategory.count()
    forCountState = Project_content.objects.filter(project_id=project_id, state=data['state'])
    stateCount = forCountState.count()

    project_contents = Project_content(
        category=data['category'],
        topic=data['topic'],
        state=data['state'],
        content='',
        category_index=categoryCount,
        state_index=stateCount,
        project_name=forProjectName.project_name,
        project_id=project_id,
        using=0
    )
    project_contents.save()

