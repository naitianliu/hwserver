from user_auth.models import BindAccount


class BindAccountHelper(object):
    def __init__(self):
        pass

    def check_new_user_by_phone(self, phone_number):
        rows = BindAccount.objects.filter(type='phone', value=phone_number)
        result = len(rows) == 0
        return result

    def check_new_user_by_wechat(self, wechat_uid):
        rows = BindAccount.objects.filter(type='wechat', value=wechat_uid)
        result = len(rows) == 0
        return result

    def get_username_by_phone(self, phone_number):
        try:
            row = BindAccount.objects.get(type='phone', value=phone_number)
            username = row.username
        except BindAccount.DoesNotExist:
            username = None
        return username

    def get_username_by_wechat(self, wechat_uid):
        try:
            row = BindAccount.objects.get(type='wechat', value=wechat_uid)
            username = row.username
            active = row.active
        except BindAccount.DoesNotExist:
            username = None
            active = False
        return username, active

    def activate_account(self, username, account_type, account_value):
        try:
            row = BindAccount.objects.get(username=username, value=account_value, type=account_type)
            row.active = True
            row.save()
            return True
        except BindAccount.DoesNotExist:
            return False

    def bind_new_account(self, username, account_type, account_value):
        rows = BindAccount.objects.filter(username=username, value=account_value, type=account_type)
        if len(rows) == 0:
            BindAccount(
                username=username,
                value=account_value,
                type=account_type,
                active=False
            ).save()