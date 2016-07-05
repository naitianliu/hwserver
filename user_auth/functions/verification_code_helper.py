from user_auth.vendors.alidayu_sms import SMSHelper
from user_auth.models import VerificationCode
from random import randint
import datetime


class VerificationCodeHelper(object):
    def __init__(self, phone_number):
        self.phone_number = phone_number
        timestamp_str = datetime.datetime.now().strftime('%s')
        self.datetime_now = int(timestamp_str)
        one_hour_ago_str = (datetime.datetime.now() - datetime.timedelta(hours=1)).strftime('%s')
        self.one_hour_ago = int(one_hour_ago_str)
        one_day_ago_str = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%s')
        self.one_day_ago = int(one_day_ago_str)

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
        rows = VerificationCode.objects.filter(phone_number=self.phone_number, code=code, created_time__gt=self.one_hour_ago)
        valid = len(rows) > 0
        error_code = 0 if valid else 1030
        return error_code

    def __generate_code(self):
        code = randint(100000, 999999)
        code = str(code)
        VerificationCode(
            phone_number=self.phone_number,
            code=code,
            created_time=self.datetime_now
        ).save()
        return code

    def __check_if_hit_limit(self):
        rows = VerificationCode.objects.filter(phone_number=self.phone_number, created_time__gt=self.one_day_ago)
        result = len(rows) > 5
        return result