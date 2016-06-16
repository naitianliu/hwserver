from django.conf.urls import url
from api.views_set.vendors import *

urlpatterns = [
    url(r'^get_sts_token/', get_sts_token)
]