import json
from mainpage.models import Projects, Project_contents, User_Project
from django.shortcuts import render

# Create your views here.
def createProject(request):
    data = json.loads(request.body)

