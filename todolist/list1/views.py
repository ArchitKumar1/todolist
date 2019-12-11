# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.shortcuts import render_to_response
from .models import *
from django.core import serializers
from django.http import HttpResponse,JsonResponse,request,response
from django.views.decorators.csrf import csrf_exempt
from .jwt_operations import encode, decode
import ast


@csrf_exempt
def login(request):
    if (request.method == 'POST'):
        data = json.loads(request.body)
        userAvailable = User.objects.filter(user_id = data.get('user_id'), password = data.get('password'))
        if(userAvailable):
            token = encode(data.get('user_id'))
            forward_url =  'main'
            return JsonResponse({'message' : 'User Authenticated', 'token' : token, 'path':forward_url }, status=202)
        else:
            return JsonResponse({'message' :'User Not Found'}, status=401)

def user_add(request):
    if(request.method == 'POST'):
        data = json.loads(request.body)
        print data
        new_user = User(name = data.get('name'), user_id = data.get('user_id'), active = data.get('active'), password = data.get('password'))
        new_user.save()
        return JsonResponse("user added",safe =False)

def group_add(request):
    if(request.method == 'POST'):
        data = json.loads(request.body)
        group_owner = User.objects.filter(user_id=data.get('user_id'))
        new_group = Group(group_id = data.get('group_id'),title = data.get('title'),user_id = group_owner[0])
        new_group.save()
        return JsonResponse("group added",safe= False)

def task_add(request):
    if(request.method == 'POST'):
        data = json.loads(request.body)
        task_owner = Group.objects.filter(group_id =data.get('group_id'))
        new_task = Task(task_id = data.get('task_id'),description = data.get('description'),status = data.get('status'),group_id = task_owner[0])
        new_task.save()
        return JsonResponse("task added",safe= False)

def user_get(request):
    if (request.method == 'POST'):
        serial = serializers.serialize('json', Task.objects.all())
        return JsonResponse(json.loads(serial), safe=False)

def group_get(request):
    if (request.method == 'POST'):
        serial = serializers.serialize('json', Task.objects.all())
        return JsonResponse(json.loads(serial), safe=False)

def task_get(request):
    if(request.method == 'POST'):
        serial = serializers.serialize('json', Task.objects.all())
        return JsonResponse(json.loads(serial), safe=False)

def task_get_from_group(request):
    print "Hello"
    if (request.method == 'POST'):
        data = json.loads(request.body)
        print data
        all_tasks = Task.objects.filter(group_id=data.get('group_id'))
        serial = serializers.serialize('json', all_tasks)
        return JsonResponse(json.loads(serial), safe=False)


# @csrf_exempt
# def task(request):
#     if (request.method == 'GET'):
#         serial = serializers.serialize('json', Task.objects.all())
#         return JsonResponse(json.loads(serial), safe=False)
#     elif (request.method == 'POST'):
#         data = json.loads(request.body)
#         newTask = Task(taskDescription=data.get('taskDescription'), taskId=data.get('taskId'),
#                         taskGroupId=data.get('taskGroupId'), taskStatus=data.get('taskStatus'))
#         newTask.save()
#         return JsonResponse("succesfully submitted", safe=False)
#     elif (request.method == 'DELETE'):
#         Task.objects.filter(taskDescription="hello").delete()
#         return JsonResponse("succesfully submitted", safe=False)

def signup(request):
    pass
def home(request):
    pass