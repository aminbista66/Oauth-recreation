from .models import AuthCode
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

def get_auth_code(user):
    auth_code = AuthCode.objects.get(user=user)
    return auth_code.code

class customClaimToken(TokenObtainPairSerializer, Token):
    @classmethod
    def get_token(cls, user, scope):
        token = super().get_token(user)
        token['scope'] = scope
        return token

class IdTokenClaim(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        return token