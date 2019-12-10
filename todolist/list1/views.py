# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.shortcuts import render_to_response
from .models import Task
from django.core import serializers
from django.http import HttpResponse,JsonResponse,request,response
from django.views.decorators.csrf import csrf_exempt
import ast

@csrf_exempt
def task(request):
    if (request.method == 'GET'):
        serial = serializers.serialize('json', Task.objects.all())
        return JsonResponse(json.loads(serial), safe=False)
    elif (request.method == 'POST'):
        data = json.loads(request.body)
        newTask = Task(taskDescription=data.get('taskDescription'), taskId=data.get('taskId'),
                        taskGroupId=data.get('taskGroupId'), taskStatus=data.get('taskStatus'))
        newTask.save()
        return JsonResponse("succesfully submitted", safe=False)
    elif (request.method == 'DELETE'):
        Task.objects.filter(taskDescription="hello").delete()
        return JsonResponse("succesfully submitted", safe=False)

def login(request):
    pass
def signup(request):
    pass
# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals
# import json
# from django.shortcuts import render_to_response
# from .models import Item
# from django.core import serializers
# from django.http import HttpResponse,JsonResponse,request,response
# from django.views.decorators.csrf import csrf_exempt
# import ast
#
# @csrf_exempt
# def view_all_items(request):
#     serial = serializers.serialize('json', Item.objects.all())
#     return JsonResponse(json.loads(serial),safe=False)
#
# @csrf_exempt
# def add_item_page(request):
#     if (request.method == 'GET'):
#         return render_to_response('a.html')
#
# @csrf_exempt
# def add_item(request):
#     if(request.method  == 'POST'):
#         print request.body
#         json_data = json.loads(request.body)
#         data1 = Item(task = json_data['task'],itemid = json_data['itemid'],checkstatus = json_data['checkstatus'])
#         data1.save()
#         serial = serializers.serialize('json',[data1,])
#         return JsonResponse(json.loads(serial),safe=False)
#
# @csrf_exempt
# def delete_item(request):
#     if(request.method  == 'GET'):
#         json_data = json.loads(request.body)
#         id = json_data['id']
#         item_To_Be_Deleted = Item.objects.filter(itemid =id )
#         Item.objects.filter(itemid = id).delete()
#         serial = serializers.serialize('json',item_To_Be_Deleted)
#         return JsonResponse(json.loads(serial),safe=False)
