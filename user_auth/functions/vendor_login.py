from user_auth.functions.bind_account_helper import BindAccountHelper
from user_auth.functions.user_helper import UserHelper
from user_auth.functions.profile_helper import ProfileHelper


class VendorLogin(object):
    def __init__(self):
        self.bind_account_helper = BindAccountHelper()
        self.user_helper = UserHelper()

    def wechat_login(self, uid, nickname, profile_img_url):
        is_new_user = self.bind_account_helper.check_new_user_by_wechat(uid)
        if is_new_user:
            username = self.user_helper.generate_username()
            self.user_helper.register(username, None)
            self.bind_account_helper.bind_new_account(username, "wechat", uid)
            ProfileHelper(username).update_profile(nickname, profile_img_url)
            token = self.user_helper.generate_token(username)
            active = False
        else:
            username, active = self.bind_account_helper.get_username_by_wechat(uid)
            ProfileHelper(username).update_profile(nickname, profile_img_url)
            token = self.user_helper.generate_token(username)
        return username, token, active