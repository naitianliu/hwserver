from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib import auth
import uuid


class UserHelper(object):
    def __init__(self):
        pass

    def generate_username(self):
        username = uuid.uuid1()
        return username

    def check_username_exists(self, username):
        rows = User.objects.filter(username=username)
        result = len(rows) > 0
        return result

    def register(self, username, password):
        if not User.objects.filter(username=username):
            user = User.objects.create_user(
                username=username,
                password=password,
            )
            user.save()

    def login(self, username, password):
        user_obj = auth.authenticate(username=username, password=password)
        result = True if user_obj else False
        return result

    def reset_password(self, username, password):
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()

    def generate_token(self, username):
        user = User.objects.get(username=username)
        token = Token.objects.get_or_create(user=user)[0].key
        return token