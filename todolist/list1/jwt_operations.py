import jwt
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
        return payload_data.user_id
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'