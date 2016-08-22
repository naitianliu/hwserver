from django.conf.urls import url
from api.views_set.classroom import *

urlpatterns = [
    url(r'^create/', create),
    url(r'^update/', update),
    url(r'^close/', close),
    url(r'^get_list/', get_list),
    url(r'^search/', search),
    url(r'^send_request/', send_request_to_join),
    url(r'^approve_request/', approve_request)
]