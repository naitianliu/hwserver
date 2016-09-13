from django.contrib import admin
from api.models import *

# Register your models here.

admin.site.register(Classroom)
admin.site.register(ClassroomMember)
admin.site.register(School)
admin.site.register(JoinClassroomRequest)
admin.site.register(Homework)
admin.site.register(Submission)
admin.site.register(Comment)