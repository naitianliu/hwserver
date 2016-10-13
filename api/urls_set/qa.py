from django.conf.urls import url
from api.views_set.qa import *

urlpatterns = [
    url(r'^question/create/', question_create),
    url(r'^question/close/', question_close),
    url(r'^question/get_list/', question_get_list),
    url(r'^answer/create/', answer_create),
    url(r'^answer/agree/', answer_agree),
    url(r'^answer/get_list/', answer_get_list),
]