from django.test import TestCase
from api.vendors.aliyun import AliyunHelper

# Create your tests here.


class AliyunTest(TestCase):
    def test_get_sts_token(self):
        print AliyunHelper().get_sts_token()