from django.conf.urls import url
from api.views_set.homework import *

urlpatterns = [
    url(r'^create/', create),
    url(r'^submit/', submit),
    url(r'^grade/', grade),
]