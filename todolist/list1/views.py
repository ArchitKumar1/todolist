# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.shortcuts import render_to_response
from .models import Item
from django.core import serializers
from django.http import HttpResponse,JsonResponse,request,response
from django.views.decorators.csrf import csrf_exempt
import ast

@csrf_exempt
def view_all_items(request):
    serial = serializers.serialize('json', Item.objects.all())
    return JsonResponse(json.loads(serial),safe=False)

@csrf_exempt
def add_item(request):

    if(request.method  == 'POST'):
        data = request.body
        pst = ast.literal_eval(data)
        ll  = []
        for ps in pst.keys():
            ll.append(pst[ps])
        data1 = Item(task=ll[0],itemid=ll[1],checkstatus=ll[2])
        data1.save()
        serial = serializers.serialize('json',[data1,])
        return JsonResponse(json.loads(serial),safe=False)

@csrf_exempt
def delete_item(request):
    if(request.method  == 'GET'):

        data = request.body
        pst = ast.literal_eval(data)
        ll = []
        for ps in pst.keys():
            ll.append(pst[ps])
        id = ll[0]
        item_To_Be_Deleted = Item.objects.filter(itemid =id )
        Item.objects.filter(itemid = id).delete()
        serial = serializers.serialize('json',item_To_Be_Deleted)
        return JsonResponse(json.loads(serial),safe=False)
