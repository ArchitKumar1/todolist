
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.shortcuts import render_to_response
from .models import User,GroupTaskMapping,Group,Task
from django.core import serializers
from django.http import HttpResponse, JsonResponse, request, response
from django.views.decorators.csrf import csrf_exempt
from .jwt_operations import encode, decode
from .random_string_generator import generate_random_string

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
        print data
        new_user = User(name=data.get('name'), user_id=data.get('user_id'), active=data.get('active'),
                        password=data.get('password'))
        new_user.save()
        return JsonResponse({"message": "User Added"}, status=201)


# this is an internal function
@csrf_exempt
def user_get(request):
    if (request.method == 'POST'):
        serial = serializers.serialize('json', Task.objects.all())
        return JsonResponse(json.loads(serial), safe=False)
