import jwt
import time

def generate_jwt_token(secret_key, payload, expiration_seconds=3600):
    payload['iat'] = int(time.time())
    payload['exp'] = int(time.time()) + expiration_seconds
    encoded_jwt = jwt.encode(payload, secret_key, algorithm="HS256")
    return encoded_jwt

