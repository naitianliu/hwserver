from django.test import TestCase
from api.notification.apns_helper import APNSHelper
from user_auth.functions.device_token_helper import DeviceTokenHelper
from api.notification.message_template import MESSAGE


class APNSHelperTest(TestCase):
    def test_send_notification(self):
        username = 'testuser'
        message = MESSAGE['requests'].format(username).encode('utf8')
        print message
        device_token = '5AA987E74BF22E688748A59A11C44E84E8AF357CB0435AEB1CADFBC2A079A20D'
        DeviceTokenHelper(username).add_update_device_token(device_token)
        APNSHelper(username).send_simple_notification(message)
