from django.test import TestCase
from api.notification.apns_helper import APNSHelper
from user_auth.functions.device_token_helper import DeviceTokenHelper
from api.notification.message_template import MESSAGE


class APNSHelperTest(TestCase):
    def test_send_notification(self):
        username = 'testuser'
        message = MESSAGE['requests'].format(username).encode('utf8')
        print message
        device_token = '5F083895D1EC4AD3052F27D429C0A93FBF6820B47467D4A2DEF095697E76BBE3'
        DeviceTokenHelper(username).add_update_device_token(device_token)
        APNSHelper(username).send_simple_notification(message)
