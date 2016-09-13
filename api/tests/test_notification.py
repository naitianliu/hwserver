from django.test import TestCase
from api.notification.apns_helper import APNSHelper
from user_auth.functions.device_token_helper import DeviceTokenHelper


class APNSHelperTest(TestCase):
    def test_send_notification(self):
        username = 'testuser'
        device_token = '5F083895D1EC4AD3052F27D429C0A93FBF6820B47467D4A2DEF095697E76BBE3'
        DeviceTokenHelper(username).add_update_device_token(device_token)
        APNSHelper(username).send_simple_notification("test!", payload_dict=dict())
