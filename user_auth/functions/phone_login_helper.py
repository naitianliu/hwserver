from user_auth.functions.verification_code_helper import VerificationCodeHelper
from user_auth.functions.bind_account_helper import BindAccountHelper
from user_auth.functions.user_helper import UserHelper


class PhoneLoginHelper(object):
    def __init__(self, phone_number):
        self.phone_number = phone_number
        self.verify_code_helper = VerificationCodeHelper(phone_number)
        self.bind_account_helper = BindAccountHelper()
        self.user_helper = UserHelper()

    def register(self, code, password):
        if self.verify_code_helper.verify_code(code) == 0:
            if self.bind_account_helper.check_new_user_by_phone(self.phone_number):
                error_code = 0
            else:
                error_code = 1050
        else:
            error_code = 1051
        if error_code == 0:
            username = self.user_helper
            self.user_helper.register(username, password)
            token = self.user_helper.generate_token(username)
        else:
            token = None
        return error_code, token

    def login(self, phone_number, password):
        username = self.bind_account_helper.get_username_by_phone(phone_number)
        if username:
            if self.user_helper.login(username, password):
                error_code = 0
            else:
                error_code = 1011
        else:
            error_code = 1010
        token = self.user_helper.generate_token(username) if error_code == 0 else None
        return token

    def reset_password(self):
        pass