from django.contrib import admin
from user_auth.models import *

# Register your models here.

admin.site.register(VerificationCode)
admin.site.register(Profile)
admin.site.register(DeviceToken)
admin.site.register(BindAccount)
