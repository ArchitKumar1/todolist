# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.shortcuts import render_to_response
from .models import User, GroupTaskMapping, Group, Task
from django.core import serializers
from django.http import HttpResponseRedirect, JsonResponse, request, response
from django.views.decorators.csrf import csrf_exempt
from .jwt_operations import encode, decode
from .random_string_generator import generate_random_string


# ================================================User Related Operators================================================#

@csrf_exempt
def login(request):
    if (request.method == 'POST'):
        data = json.loads(request.body)
        userAvailable = User.objects.filter(user_id=data.get('user_id'), password=data.get('password'))
        if (userAvailable):
            token = encode(data.get('user_id'))
            forward_url = 'main'
            return JsonResponse({'message': 'User Authenticated', 'token': token, 'path': forward_url}, status=202)
        else:
            return JsonResponse({'message': 'User Not Found'}, status=401)


@csrf_exempt
def user_add(request):
    if (request.method == 'POST'):
        data = json.loads(request.body)
        if len(list(User.objects.filter(user_id=data.get('user_id')))) == 0:
            new_user = User(name=data.get('name'), user_id=data.get('user_id'), active=data.get('active'),
                            password=data.get('password'))
            new_user.save()
            return JsonResponse({"message": "User Added"}, status=201)
        else:
            return JsonResponse({'message': 'User ID Already exist'}, status=400)


@csrf_exempt
def get_all_users(request):
    if (request.method == 'GET'):
        user_id = decode(request)
        if (user_id == None):
            return HttpResponseRedirect("http://192.168.37.36:5500/")
        all_users = list(User.objects.all().exclude(user_id=user_id).values('user_id'))
        return JsonResponse({"users": all_users}, status=200)


@csrf_exempt
def change_password(request):
    if (request.method == 'PATCH'):
        try:
            data = json.loads(request.body)
            new_password = data.get('password')
            user_id = decode(request)
            if (user_id == None):
                return HttpResponseRedirect("http://192.168.37.36:5500/")
            user = User.objects.filter(user_id=user_id)
            user.update(password=new_password)
            return JsonResponse({'message': 'Password Updated'}, status=202)
        except:
            return JsonResponse({'message': 'Error Occured'}, status=401)


# ================================================Group Related Operators================================================#


@csrf_exempt
def group_add(request):
    if (request.method == 'POST'):
        user_id = decode(request)
        if (user_id == None):
            return HttpResponseRedirect("http://192.168.37.36:5500/")
        group_owner = User.objects.filter(user_id=user_id)
        data = json.loads(request.body)
        group_id_new = generate_random_string()
        new_group = Group(group_id=group_id_new, title=data.get('group_title'), user_id=group_owner[0])
        new_group.save()
        return JsonResponse({'message': "group added"}, status=201)


def group_get(request):
    if (request.method == "GET"):
        user_id = decode(request)
        if (user_id == None):
            return HttpResponseRedirect("http://192.168.37.36:5500/")
        groups_public_owner = Group.objects.filter(type="1", user_id=user_id).values('pk', 'title')
        groups_public_not_owner = Group.objects.filter(type="1").exclude(user_id=user_id).values('group_id', 'title')
        groups_personal = Group.objects.filter(user_id=user_id, type="2").values('pk', 'title')
        groups_private_owner = Group.objects.filter(user_id=user_id, type="0").values('pk', 'title')
        groups_private_not_owner = GroupTaskMapping.objects.filter(user_id=user_id).values('title', 'group_id')

        owner = list(groups_private_owner) + list(groups_public_owner) + list(groups_personal)
        not_owner = list(groups_public_not_owner) + list(groups_private_not_owner)
        return JsonResponse({"owner": owner, "not_owner": not_owner}, status=200, safe=False)


def group_delete(request):
    if request.method == 'DELETE':
        user_id = decode(request)
        if (user_id == None):
            return HttpResponseRedirect("http://192.168.37.36:5500/")
        data = json.loads(request.body)
        group = Group.objects.filter(group_id=data.get('group_id'), user_id=user_id)
        if len(list(group)) == 0:
            return JsonResponse({"message": "Only owner can delete the group!"}, status=401)
        group_title = group.values('title')
        group.delete()
        group = GroupTaskMapping.objects.filter(group_id=data.get('group_id'))
        group.delete()
        return JsonResponse({"message": "Group Deleted", "title": list(group_title)}, status=202)


# ================================================Task Related Operators================================================#


@csrf_exempt
def task_add(request, groupid):
    if (request.method == 'POST'):
        data = json.loads(request.body)
        task_id_new = generate_random_string()
        task_owner = Group.objects.filter(group_id=groupid)
        new_task = Task(task_id=task_id_new, description=data.get('task_description'), group_id=task_owner[0])
        new_task.save()
        return JsonResponse({"message": "Task Added"}, status=201)


@csrf_exempt
def task_get(request, groupid):
    if request.method == 'GET':
        user_id = decode(request)
        if (user_id == None):
            return HttpResponseRedirect("http://192.168.37.36:5500/")
        tasks = Task.objects.filter(group_id=groupid).values('pk', 'description', 'status')
        return JsonResponse(list(tasks), status=200, safe=False)


def task_delete(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        task = Task.objects.filter(task_id=data.get('task_id'))
        task.delete()
        return JsonResponse({"message": "Task Deleted"}, status=202)


def change_task_status(request):
    if request.method == "PATCH":
        data = json.loads(request.body)
        task = Task.objects.filter(task_id=data.get('task_id')).update(status=data.get('task_status'))
        return JsonResponse({"message": "Status Changed"}, status=202)


# ================================================Group share  Related Operators================================================#

def share_group(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        group_id = data.get('group_id')
        user_id = decode(request)
        if (user_id == None):
            return HttpResponseRedirect("http://192.168.37.36:5500/")
        group_object = Group.objects.filter(group_id=group_id, user_id=user_id)
        if (len(list(group_object)) == 0):
            return JsonResponse({"message": "Only owner can change this property!"}, status=401)
        group_name = list(group_object.values('title'))[0].get("title")
        all_checked = data.get('all_checked')
        if all_checked == True:
            group_object.update(type='1')
            GroupTaskMapping.objects.filter(group_id=group_id).delete()
        else:
            user_ids = data.get('user_ids')
            group_object.update(type='0')
            GroupTaskMapping.objects.filter(group_id=group_id).delete()
            for user in list(user_ids):
                new_GroupTaskMapping = GroupTaskMapping(user_id=str(user), group_id=group_id, title=group_name)
                new_GroupTaskMapping.save()
        return JsonResponse({"message": "Share enabled"}, status=202)


def home(request):
    pass
