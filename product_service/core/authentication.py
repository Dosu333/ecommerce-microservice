from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings

class JWTUser:
    def __init__(self, payload):
        self.id = payload.get('id')
        self.fullname = payload.get('fullname')
        self.email = payload.get('email')
        self.roles = payload.get('roles')
        
    def is_authenticated(self):
        return True

class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]

        try:
            decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired", code='token_expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token", code='invalid_token')

        user = self.get_user(decoded_token)
        return (user, decoded_token)
    
    def get_user(self, decoded_token):
        return JWTUser(decoded_token)
