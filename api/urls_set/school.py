from django.conf.urls import url
from api.views_set.school import *

urlpatterns = [
    url(r'^create/', school_create),
    url(r'^get_list/', school_get_list),
    url(r'^update/', school_update),
    url(r'^close/', school_close),
]