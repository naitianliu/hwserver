from django.test import TestCase
from user_auth.vendors.alidayu_sms import SMSHelper

# Create your tests here.


class SMSTest(TestCase):
    def test_send_verification_code(self):
        phone_number = '13886020732'