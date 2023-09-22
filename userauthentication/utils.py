from rest_framework.authtoken.models import Token

def get_token_by_user(user):
    token = Token.objects.create(user = user)
    return token.key