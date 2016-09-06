from django.conf.urls import url
from api.views_set.updates import *

urlpatterns = [
    url(r'^get/', get_updates)
]