import jwt
from django.http import JsonResponse
import json
from todolist.settings import SECRET_KEY_JWT, JWT_ALGORITHM

def encode(user_id, expiry=1200):
    payload_data = {
        'user_id' : user_id,
        'exp' : expiry
    }
    token = jwt.encode(payload_data, SECRET_KEY_JWT, algorithm=JWT_ALGORITHM)
    return token

def decode(token):
    try:
        payload_data = jwt.decode(token, SECRET_KEY_JWT)
        print payload_data
        return payload_data.user_id
    except jwt.ExpiredSignatureError:
        return JsonResponse({'message':'Signature expired. Please log in again.'}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({'message':'Invalid token. Please log in again.'}, status=401)
    return null

def authorize(request):
    headers = json.loads(request.headers)
    user_id = decode(headers.get('Authorization'))
    return user_id