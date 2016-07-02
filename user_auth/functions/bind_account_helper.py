from user_auth.models import BindAccount


class BindAccountHelper(object):
    def __init__(self):
        pass

    def check_new_user_by_phone(self, phone_number):
        rows = BindAccount.objects.filter(type='phone', value=phone_number)
        result = len(rows) == 0
        return result

    def get_username_by_phone(self, phone_number):
        try:
            row = BindAccount.objects.get(type='phone', value=phone_number)
            username = row.username
        except BindAccount.DoesNotExist:
            username = None
        username
