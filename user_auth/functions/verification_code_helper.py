from user_auth.vendors.alidayu_sms import SMSHelper
from user_auth.models import VerificationCode
from random import randint
import datetime


class VerificationCodeHelper(object):
    def __init__(self, phone_number):
        self.phone_number = phone_number

    def send_code(self):
        if self.__check_if_hit_limit():
            error_code = 1020
        else:
            code = self.__generate_code()
            print code
            SMSHelper().send_code_via_sms(self.phone_number, code)
            error_code = 0
        return error_code

    def verify_code(self, code):
        one_hour_ago = datetime.datetime.now() - datetime.timedelta(hours=1)
        rows = VerificationCode.objects.filter(phone_number=self.phone_number, code=code, created_time__gt=one_hour_ago)
        valid = len(rows) > 0
        error_code = 0 if valid else 1030
        return error_code

    def __generate_code(self):
        code = randint(100000, 999999)
        code = str(code)
        VerificationCode(
            phone_number=self.phone_number,
            code=code
        ).save()
        return code

    def __check_if_hit_limit(self):
        one_day_ago = datetime.datetime.now() - datetime.timedelta(days=1)
        rows = VerificationCode.objects.filter(phone_number=self.phone_number, created_time__gt=one_day_ago)
        result = len(rows) > 5
        return result