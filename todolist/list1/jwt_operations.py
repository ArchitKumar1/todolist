import jwt
from django.http import request,JsonResponse
import json
from todolist.settings import SECRET_KEY_JWT, JWT_ALGORITHM

def encode(user_id):
    payload_data = {
        'user_id' : user_id
    }
    token = jwt.encode(payload_data, SECRET_KEY_JWT, algorithm=JWT_ALGORITHM)
    return token

def decode(request):
    try:
        authorization_header = request.META.get('HTTP_AUTHORIZATION')
        token = authorization_header.split()[1]
        payload_data = jwt.decode(token, SECRET_KEY_JWT, algorithm=JWT_ALGORITHM)
        return payload_data.get('user_id')
    except jwt.ExpiredSignatureError:
        return JsonResponse({'message':'Signature expired. Please log in again.'}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({'message':'Invalid token. Please log in again.'}, status=401)
    return null
