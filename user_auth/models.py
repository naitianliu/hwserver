from __future__ import unicode_literals

from django.db import models

# Create your models here.


class VerificationCode(models.Model):
    phone_number = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    created_time = models.IntegerField()

    def __unicode__(self):
        return self.phone_number


class Profile(models.Model):
    username = models.CharField(max_length=50)
    nickname = models.CharField(max_length=100, blank=True, null=True)
    img_url = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.username


class BindAccount(models.Model):
    username = models.CharField(max_length=50)
    type = models.CharField(max_length=20)
    value = models.CharField(max_length=50)
    active = models.BooleanField(default=False)


class DeviceToken(models.Model):
    username = models.CharField(max_length=200)
    token = models.CharField(max_length=200)
    updated_time = models.IntegerField()

    def __unicode__(self):
        return self.username
