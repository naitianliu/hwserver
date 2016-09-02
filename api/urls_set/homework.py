from django.conf.urls import url
from api.views_set.homework import *

urlpatterns = [
    url(r'^create/', create),
    url(r'^submit/', submit),
    url(r'^grade/', grade),
    url(r'^close/', close),
    url(r'^get_homework_list/', get_homework_list),
    url(r'^get_submission_list/', get_submission_list),
]