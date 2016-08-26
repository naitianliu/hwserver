from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Classroom(models.Model):
    uuid = models.CharField(max_length=50)
    name = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    creator = models.CharField(max_length=200)
    school_uuid = models.CharField(max_length=50)
    code = models.CharField(max_length=20)
    active = models.BooleanField(default=True)
    created_timestamp = models.IntegerField()
    updated_timestamp = models.IntegerField()

    def __unicode__(self):
        return self.name


class School(models.Model):
    uuid = models.CharField(max_length=50)
    name = models.CharField(max_length=500)
    creator = models.CharField(max_length=200)
    location_x = models.FloatField(null=True, blank=True)
    location_y = models.FloatField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    created_timestamp = models.IntegerField()
    updated_timestamp = models.IntegerField()

    def __unicode__(self):
        return self.name


class ClassroomMember(models.Model):
    classroom_uuid = models.CharField(max_length=50)
    user_id = models.CharField(max_length=200)
    role = models.CharField(max_length=10)
    active = models.BooleanField(default=True)
    created_timestamp = models.IntegerField()
    updated_timestamp = models.IntegerField()

    def __unicode__(self):
        return self.user_id


class JoinClassroomRequest(models.Model):
    uuid = models.CharField(max_length=50)
    classroom_uuid = models.CharField(max_length=50)
    requester = models.CharField(max_length=200)
    role = models.CharField(max_length=10)
    comment = models.TextField(null=True, blank=True)
    approver = models.CharField(max_length=200, null=True, blank=True)
    """status: pending, approved, rejected"""
    status = models.CharField(max_length=10)
    created_timestamp = models.IntegerField()
    updated_timestamp = models.IntegerField()

    def __unicode__(self):
        return self.requester


