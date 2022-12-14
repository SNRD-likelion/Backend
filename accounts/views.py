from django.shortcuts import render
import jwt
import bcrypt
import json


from .models import User
from mainpage.models import Projects, User_Project, Project_content

from sunaropdaback.settings import SECRET_KEY  # 로컬이랑 배포일 때 좀 다른 느낌
from django.http import HttpResponse, JsonResponse

def register(request):
    data = json.loads(request.body)

    try:
        if User.objects.filter(email=data['email']).exists():
            return JsonResponse({"message": "EXISTS_EMAIL"}, status=400)

        User.objects.create(
            email = data['email'],
            password= bcrypt.hashpw(data["password"].encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8"),
            name = data['name'],
            information = "나이를 입력하세요, 파트를 입력하세요, 학교/회사 이름을 입력해주세요, 나를 표현하는 한줄을 적어주세요"
        ).save()

        project = Projects(
            project_name=data['email']+"님의 프로젝트",
            slogan="프로젝트 슬로건",
            duration="프로젝트 기간"
        )
        project.save()

        ppp=Projects.objects.get(project_name=data['email']+"님의 프로젝트", createdAt=project.createdAt)
        user_project = User_Project(
            project_id=ppp,
            email=User.objects.get(email=data['email'])
        )
        user_project.save()

        # PM = ['아이디어', '타겟과 목적', '목표가 아닌 것', '시장조사', '서비스의 배경', '유사한 서비스 탐구', '비즈니스 모델']
        # Design = ['스케치', '무드보드', '와이어프레임', '프로토타입']
        # Frontend = ['개발도구 선정', '개발환경세팅', '페이지별 진행상황', '메인화면', '통신 및 테스트', '배포']
        # Backend = ['세부기능 구성', '데이터모델링', '개발도구 선정', '개발환경세팅', 'DB구축', '기능구현', '피드백 및 수정', '배포', '통신 및 테스트']
        # PM_contents = [
        #     "일상 속에서 느끼는 불편함😬은 무엇이 있는지 팀원들과 이야기해보세요 \n \n 우리의 서비스로 해결할 수 있는 것을  무엇이 있을까요? \n혹은 여러분이 만들고 싶은 서비스가 있을까요? \n팀원들과 함께 어떤 이야기든 차근차근 모아봅시다 \n※ 가장 중요한 포인트는 실현 가능성과 개발 가능성입니다!",
        #     "아이디어를 정했다면 \n이제 아이디어의 타겟은 누구인지 정해봅시다. \n타겟의 범위에 따라 서비스의 역할이 달라지니까요. \n ex) 성인 남녀 20~30대 / 대학생 / \n 이 서비스를 통해서 무엇을 얻고 싶은가요? \n한 문장으로 정의할 수 있는 서비스가 좋은 서비스랍니다.",
        #     "\'목표가 아닌 것\' 이란 프로젝트에 연관되어 만들어볼 수는 있는 기능 혹은 서비스이지만, 목표에 정확하게 일치하지 않기에 의도적으로 하지 않거나 해결하지 않기로 미리 결정하는 것입니다 \n 이를 통해 여러분 하고자 하는 서비스의 범위를 제한하세요 \n 왜냐하면 “목표가 아닌 것”까지 만들려고 하면, 프로젝트가 늘어지거나 업무가 폭발해 해결할 수 없는 문제들이 발생할 수 있습니다. 목표가 아닌 것을 잘 정의해야 \'이것도 같이 하면 좋겠다\'는 의견에 휘둘리지 않을 수 있습니다",
        #     "여러분이 만들어나갈 서비스의 배경을 한번 이야기 해 봅시다. \n배경이란 여러분이 왜 이 서비스를 만들었는지, 어떤 걸 이루고 싶은지를 정리하는 부분입니다. \n아이디어를 기반으로 해서, 어떤 서비스를 만들고 싶은지를 가볍게 정리해 봅시다.\n서비스의 배경을 통해서, 사람들에게 왜 이 서비스가 필요한지를 이야기해 주세요.  ",
        #     "여러분의 서비스를 과연 사람들이 원하는지, 어떻게 생각하는지 \n시장 조사를 직접 만들어서 시작해보세요. \n 여러분이 설정했던 타겟들에게 설문조사를 진행하세요.\n예상하는 서비스에 대하여 사람들이 만족하는지, \n사용할 의사가 있는지, 한계점은 무엇이라고 생각하는지 파악하세요.\n사람들의 기대와 고민을 기반으로 서비스를 발전시켜 보세요.",
        #     "다른 유사한 서비스들을 분석해보세요.\n그 서비스들은 어떤 장점이 있는지, 단점이 있는지를 정리하세요.\n그 분석을 기반으로 해서 여러분의 서비스만의 차별점을 만들어보세요.  ",
        #     "어떤 서비스든 유지를 위해서는 수익이 필요합니다. \n여러분의 서비스는 어떻게 하여 돈을 벌 수 있을까요?\n광고를 받거나, 서비스를 팔거나, 구독 서비스를 제공할 수도 있겠죠?\n독창적인 비즈니스 모델은 서비스의 확장성과 지속성을 올려줍니다. \n여러분만의 비즈니스 모델을 개발해 보세요!"]
        # Design_contents = [
        #     "화면을 손으로 그려서 틀을 잡아보아요!\n정밀하게 그릴 필요는 없습니다. \n여러분이 원하는 서비스의 가장 기본적인 형태의 틀을 만들어 보세요. \n나무보단 숲을 보는 단계입니다!",
        #     "무드보드에서 우리 서비스의 메인 색상과 분위기를 설정해보아요!\n구체적으로 무드보드를 만들 수록, 앞으로의 디자인을 발견시키기 수월하답니다. \n사진이나 그림등을 통해 컨셉을 정해도 좋아요",
        #     "Fiama와 adobe와 같은 툴을 이용해 화면을 그려보아요\n화면들이 어떤 식으로 구성되는지에  대하여 고민해봅시다.\n섬세한 와이어프레임의 구성이 여러분의 서비스의 퀄리티를 올려줍니다.",
        #     "여러분의 서비스가 어떻게 작동하는지, 어떤 버튼을 누르면 \n어디로 이동 하는지를 하나하나 정해보세요! \n 구체적으로 와이어프레임을 만들 수록, 개발 팀의 입장에서 \n서비스를 만들어가기가 수월해집니다."]
        # Frontend_contents = ["이번 프로젝트에 어떤 라이브러리나 프레임 워크를 사용할지 고민해보고 \n작성해주세요.개발을 진행하면서 추가해도 좋습니다!",
        #                      "개발환경을 세팅하고 라우터 구조를 고민해 봅시다.\nGITHUB을 사용한다면 repository를 만들고링크를 남겨주세요!",
        #                      "페이지별 진행상황을 사진과 함께 알려주세요. \n화면별로 새로운 작업을 생성하여 자유롭게 팀원들과 공유하세요! \n진행상황을 계속해서 업데이트하면 팀원들이 확인하고 피드백 해줄거에요! \n피드백을 받고 이를 반영해 다시 개발을 반복하는 과정은 애자일 방법론의 기본입 \n니다.",
        #                      "메인 화면 개발의 진행상황을 사진과 설명으로 팀원들에게 공유해주세요.\n이처럼 각각의 화면들 마다 작업을 생성해주세요!",
        #                      "백엔드와의 통신 및 기능 테스트를 하며 수정과 보완을 반복하며 완성해봅시다!통신을 하며 고칠 점들을 하나씩 해결하며 그 과정을 기록해보세요. 좋은 밑거름이 될 거에요!",
        #                      "완성된 기능들을 배포하여 외부에서도 페이지에 접속하고 기능을 사용해 볼 수 있도록 해야합니다.  배포를 완료하고 url을 남겨주세요!"]
        # Backend_contents = ["기획 과정에서 도출된 요구 사항을 실현하고자 필요한 세부 기능을 고민해봅시다",
        #                     "데이터베이스를 구축하기 전에 데이터 흐름을 파악하고 설계도를 구상해봅시다!\n구체적인 설계도의 구상이 개발의 속도를 높여줍니다!",
        #                     "개발 도구에 따라 프로젝트의 개발 방향이 달라질 수 있습니다. \n프로젝트에 적합할 프로그래밍 언어와 개발 환경, 프레임 워크, DBMS 등을 결정해 \n봅시다! ",
        #                     "개발을 시작하기에 앞서 개발환경을 세팅해봅시다!",
        #                     "데이터들을 담아 넣는데에 필요한 데이터 테이블들을 구축해봅시다!",
        #                     "API를 구현하여 서버가 동작하도록 하는 과정입니다. \n구상했던 기능을 직접 코드를통해 구현해봅시다!",
        #                     "피드백을 받고 이를 반영해 다시 개발을 반복하는 과정은 애자일 방법론의 기본입니다. 팀원들과 소통을 통해 피드백을 받아 구현한 기능이나 DB를 수정해봅시다!",
        #                     "완성된 기능들을 배포하여 외부에서도 기능을 직접 사용하고 데이터에 접근할 수 있도록 해야합니다. 인프라, 플랫폼과 같은 배포방식을 선정하고 절차에 맞게 배포해봅시다!",
        #                     "프론트와의 통신 및 기능 테스트를 하며 수정과 보완을 반복하며 완성해봅시다!"]

        PM = ['아이디어', '타겟과 목적', '목표가 아닌 것', '시장조사', '서비스의 배경', '유사한 서비스 탐구', '비즈니스 모델']
        Design = ['스케치', '무드보드', '와이어프레임', '프로토타입']
        Frontend = ['개발도구 선정', '개발환경세팅', '페이지별 진행상황', '메인화면', '통신 및 테스트', '배포']
        Backend = ['세부기능 구성', '데이터모델링', '개발도구 선정', '개발환경세팅', 'DB구축', '기능구현', '피드백 및 수정', '배포', '통신 및 테스트']
        PM_contents = [
            '💡일상 속에서 느끼는 불편함😬은 무엇이 있는지 팀원들과 이야기해보세요 \n \n 💬우리의 서비스로 해결할 수 있는 것을  무엇이 있을까요? \n혹은 여러분이 만들고 싶은 서비스가 있을까요? \n팀원들과 함께 어떤 이야기든 차근차근 모아봅시다 📚 \n※ 가장 중요한 포인트는 실현 가능성과 개발 가능성입니다!',
            '💡  아이디어를 정했다면 \n이제 아이디어의 타겟🧐은 누구인지 정해봅시다. \n타겟의 범위에 따라 서비스의 역할이 달라지니까요. \n ex) 성인 남녀 20~30대 / 대학생 / \n💡 이 서비스를 통해서 무엇을 얻고 싶은가요? \n한 문장으로 정의할 수 있는 서비스가 좋은 서비스랍니다.',
            '🛑 “목표가 아닌 것” 이란 프로젝트에 연관되어 만들어볼 수는 있는 기능 혹은 서비스이지만, 목표에 정확하게 일치하지 않기에 의도적으로 하지 않거나 해결하지 않기로 미리 결정하는 것입니다 \n🛑 이를 통해 여러분 하고자 하는 서비스의 범위를 제한하세요 \n🛑 왜냐하면 “목표가 아닌 것”까지 만들려고 하면, 프로젝트가 늘어지거나 업무가 폭발해 해결할 수 없는 문제들이 발생할 수 있습니다. 목표가 아닌 것을 잘 정의해야 \'이것도 같이 하면 좋겠다\'는 의견에 휘둘리지 않을 수 있습니다',
            '💡여러분이 만들어나갈 서비스의 배경을 한번 이야기 해 봅시다. \n배경이란 여러분이 왜 이 서비스를 만들었는지, 어떤 걸 이루고 싶은지를 정리하는 부분입니다. \n아이디어를 기반으로 해서, 어떤 서비스를 만들고 싶은지를 가볍게 정리해 봅시다.\n서비스의 배경을 통해서, 사람들에게 왜 이 서비스가 필요한지를 이야기해 주세요.  ',
            '💡 여러분의 서비스를 과연 사람들이 원하는지, 어떻게 생각하는지 \n시장 조사를 직접 만들어서 시작해보세요. \n💬 여러분이 설정했던 타겟들에게 설문조사를 진행하세요.\n예상하는 서비스에 대하여 사람들이 만족하는지, \n사용할 의사가 있는지, 한계점은 무엇이라고 생각하는지 파악하세요.\n사람들의 기대와 고민을 기반으로 서비스를 발전시켜 보세요.',
            '📊 다른 유사한 서비스들을 분석해보세요.\n그 서비스들은 어떤 장점이 있는지, 단점이 있는지를 정리하세요.\n그 분석을 기반으로 해서 여러분의 서비스만의 차별점을 만들어보세요.  ',
            '💸어떤 서비스든 유지를 위해서는 수익이 필요합니다. \n여러분의 서비스는 어떻게 하여 돈을 벌 수 있을까요?\n광고를 받거나, 서비스를 팔거나, 구독 서비스를 제공할 수도 있겠죠?\n💡독창적인 비즈니스 모델은 서비스의 확장성과 지속성을 올려줍니다. \n여러분만의 비즈니스 모델을 개발해 보세요!']
        Design_contents = [
            '✏화면을 손으로 그려서 틀을 잡아보아요!\n정밀하게 그릴 필요는 없습니다. \n여러분이 원하는 서비스의 가장 기본적인 형태의 틀을 만들어 보세요. \n나무🌲보단 숲🏕️ 을 보는 단계입니다!',
            '🖼️ 무드보드에서 우리 서비스의 메인 색상과 분위기를 설정해보아요!\n구체적으로 무드보드를 만들 수록, 앞으로의 디자인을 발견시키기 수월하답니다. \n사진이나 그림등을 통해 컨셉을 정해도 좋아요',
            '📇 Fiama와 adobe와 같은 툴을 이용해 화면을 그려보아요\n화면들이 어떤 식으로 구성되는지에  대하여 고민해봅시다.\n섬세한 와이어프레임의 구성이 여러분의 서비스의 퀄리티를 올려줍니다.',
            '💡  여러분의 서비스가 어떻게 작동하는지, 어떤 버튼을 누르면 \n어디로 이동 하는지를 하나하나 정해보세요! \n👉  구체적으로 와이어프레임을 만들 수록, 개발 팀의 입장에서 \n서비스를 만들어가기가 수월해집니다.']
        Frontend_contents = ['📝이번 프로젝트에 어떤 라이브러리나 프레임 워크를 사용할지 고민해보고 \n작성해주세요.개발을 진행하면서 추가해도 좋습니다!',
                             '🖥️개발환경을 세팅하고 라우터 구조를 고민해 봅시다.\nGITHUB을 사용한다면 repository를 만들고링크를 남겨주세요!',
                             '📈페이지별 진행상황을 사진과 함께 알려주세요. \n화면별로 새로운 작업을 생성하여 자유롭게 팀원들과 공유하세요! \n진행상황을 계속해서 업데이트하면 팀원들이 확인하고 피드백 해줄거에요! \n피드백을 받고 이를 반영해 다시 개발을 반복하는 과정은 애자일 방법론의 기본입 \n니다.',
                             '📇메인 화면 개발의 진행상황을 사진과 설명으로 팀원들에게 공유해주세요.\n이처럼 각각의 화면들 마다 작업을 생성해주세요!',
                             '📢백엔드와의 통신 및 기능 테스트를 하며 수정과 보완을 반복하며 완성해봅시다!통신을 하며 고칠 점들을 하나씩 해결하며 그 과정을 기록해보세요. 좋은 밑거름이 될 거에요!',
                             '완성된 기능들을 배포하여 외부에서도 페이지에 접속하고 기능을 사용해 볼 수 있도록 해야합니다.  배포를 완료하고 url을 남겨주세요!']
        Backend_contents = ['🧑‍💻기획 과정에서 도출된 요구 사항을 실현하고자 필요한 세부 기능을 고민해봅시다',
                            '📝데이터베이스를 구축하기 전에 데이터 흐름을 파악하고 설계도를 구상해봅시다!\n구체적인 설계도의 구상이 개발의 속도를 높여줍니다!',
                            '💻 개발 도구에 따라 프로젝트의 개발 방향이 달라질 수 있습니다. \n프로젝트에 적합할 프로그래밍 언어와 개발 환경, 프레임 워크, DBMS 등을 결정해 \n봅시다! ',
                            '🧑‍💻개발을 시작하기에 앞서 개발환경을 세팅해봅시다!',
                            '💾데이터들을 담아 넣는데에 필요한 데이터 테이블들을 구축해봅시다!',
                            ' 📠API를 구현하여 서버가 동작하도록 하는 과정입니다. \n구상했던 기능을 직접 코드를통해 구현해봅시다!',
                            ' 📨피드백을 받고 이를 반영해 다시 개발을 반복하는 과정은 애자일 방법론의 기본입니다. 팀원들과 소통을 통해 피드백을 받아 구현한 기능이나 DB를 수정해봅시다!',
                            '👩‍💻완성된 기능들을 배포하여 외부에서도 기능을 직접 사용하고 데이터에 접근할 수 있도록 해야합니다. 인프라, 플랫폼과 같은 배포방식을 선정하고 절차에 맞게 배포해봅시다!',
                            '💡프론트와의 통신 및 기능 테스트를 하며 수정과 보완을 반복하며 완성해봅시다!']

        # PM에 미리 넣어주기
        i = 0
        forCount = Project_content.objects.filter(state='todo')
        j = forCount.count()
        while i < 7:
            project_contents = Project_content(
                category='PM',
                topic=PM[i],
                state='todo',
                contents=PM_contents[i],
                category_index=i,
                state_index=j,
                project_name=ppp,
                project_id=ppp,
                using=0
            )
            project_contents.save()
            i = i + 1
            j = j + 1

        # Design에 미리 넣어주기
        i = 0
        while i < 4:
            project_contents = Project_content(
                category='Design',
                topic=Design[i],
                state='todo',
                contents=Design_contents[i],
                category_index=i,
                state_index=j,
                project_name=ppp,
                project_id=ppp,
                using=0
            )
            project_contents.save()
            i = i + 1
            j = j + 1

        # Front에 미리 넣어주기
        i = 0
        while i < 6:
            project_contents = Project_content(
                category='Frontend',
                topic=Frontend[i],
                state='todo',
                contents=Frontend_contents[i],
                category_index=i,
                state_index=j,
                project_name=ppp,
                project_id=ppp,
                using=0
            )
            project_contents.save()
            i = i + 1
            j = j + 1

        # Back에 미리 넣어주기
        i = 0
        while i < 9:
            project_contents = Project_content(
                category='Backend',
                topic=Backend[i],
                state='todo',
                contents=Backend_contents[i],
                category_index=i,
                state_index=j,
                project_name=ppp,
                project_id=ppp,
                using=0
            )
            project_contents.save()
            i = i + 1
            j = j + 1

        return JsonResponse({"message" : "회원가입성공"}, status=200)

    except KeyError:
        return JsonResponse({"message" : "INVALID_KEYS"}, status=400)


def login(request):
    data = json.loads(request.body)

    try:
        if User.objects.filter(email=data['email']).exists():
            user = User.objects.get(email=data['email'])

            if bcrypt.checkpw(data["password"].encode('UTF-8'), user.password.encode('UTF-8')):
                token = jwt.encode({'user': user.email}, SECRET_KEY, algorithm='HS256')
                # .decode('UTF-8')


                return JsonResponse({"token": token, "id": user.id}, status=200)

            return HttpResponse(status=401)

        return HttpResponse(status=400)

    except KeyError:
        return JsonResponse({'message': "INVALID_KEYS"}, status=400)

def logout(request):
    data = json.loads(request.body)

    try:
        if User.objects.filter(email=data["email"]).exists():
            return JsonResponse({"message": "logout!"}, status=200)



        return HttpResponse(status=400)

    except KeyError:
        return JsonResponse({'message': "Fail"}, status=400)
