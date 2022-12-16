from django.shortcuts import render
import jwt
import bcrypt
import json

from .models import User

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
            name = data['name']
        ).save()

        return JsonResponse({"message" : "회원가입성공"}, status=200)

    except KeyError:
        return JsonResponse({"message" : "INVALID_KEYS"}, status=400)


def login(request):
    data = json.loads(request.body)

    try:
        if User.objects.filter(email=data["email"]).exists():
            user = User.objects.get(email=data["email"])

            if bcrypt.checkpw(data["password"].encode('UTF-8'), user.password.encode('UTF-8')):
                token = jwt.encode({'user': user.id}, SECRET_KEY, algorithm='HS256')
                # .decode('UTF-8')

                return JsonResponse({"token": token}, status=200)

            return HttpResponse(status=401)

        return HttpResponse(status=400)

    except KeyError:
        return JsonResponse({'message': "INVALID_KEYS"}, status=400)

def logout(request):
    data = json.loads(request.body)

    try:
        if User.objects.filter(email=data["email"]).exists():
            return JsonResponse({"token": ""}, status=200)



        return HttpResponse(status=400)

    except KeyError:
        return JsonResponse({'message': "Fail"}, status=400)
