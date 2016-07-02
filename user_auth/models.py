from __future__ import unicode_literals

from django.db import models

# Create your models here.


class VerificationCode(models.Model):
    phone_number = models.CharField(max_length=30)
    code = models.CharField(max_length=10)
    created_time = models.DateTimeField(auto_now=True)


class Profile(models.Model):
    username = models.CharField(max_length=50)
    nickname = models.CharField(max_length=100)
    img_url = models.TextField()


class BindAccount(models.Model):
    username = models.CharField(max_length=30)
    type = models.CharField(max_length=20)
    value = models.CharField(max_length=50)