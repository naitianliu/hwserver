from django.conf.urls import url
from api.views_set.comment import *

urlpatterns = [
    url(r'^create/', create),
    url(r'^get_list/', get_list),
]