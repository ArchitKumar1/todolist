# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.shortcuts import render
from .models import Item
from django.core import serializers
from django.http import HttpResponse,JsonResponse,request,response
from django.views.decorators.csrf import csrf_exempt
import ast

@csrf_exempt
def view_all_items(request):
    serial = serializers.serialize('json', Item.objects.all())
    return JsonResponse(json.loads(serial),safe=False)
#
@csrf_exempt
def add_item(request):
    if(request.method  == 'POST'):
        data = request.body
        pst = ast.literal_eval(data)
        ll  = []
        for ps in pst.keys():
            ll.append(pst[ps])
        data = Item(task=ll[0],itemid=ll[1],checkstatus=ll[2])
        data.save()
        return JsonResponse("succesfully submitted",safe=False)

def delete_item(request):
    if(request.method  == 'GET'):

        Item.objects.filter(task = "hello").delete()
        return JsonResponse("succesfully submitted",safe=False)
