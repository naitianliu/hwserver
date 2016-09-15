from django.test import TestCase
from api.vendors.aliyun import AliyunHelper
from api.functions.homework_helper import HomeworkHelper

# Create your tests here.


class AliyunTest(TestCase):
    def test_get_sts_token(self):
        print AliyunHelper().get_sts_token()
