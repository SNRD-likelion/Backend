import json

from django.shortcuts import render

# Create your views here.
def createProject(request):
    data = json.loads(request.body)

