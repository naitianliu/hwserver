from user_auth.models import DeviceToken
import datetime


class DeviceTokenHelper(object):
    def __init__(self, username):
        self.username = username
        timestamp_str = datetime.datetime.now().strftime('%s')
        self.datetime_now = int(timestamp_str)

    def add_update_device_token(self, device_token):
        try:
            row = DeviceToken.objects.get(username=self.username)
            row.token = device_token
            row.updated_time = self.datetime_now
            row.save()
        except DeviceToken.DoesNotExist:
            DeviceToken(
                username=self.username,
                token=device_token,
                updated_time=self.datetime_now
            ).save()

    def get_device_token(self):
        try:
            row = DeviceToken.objects.get(username=self.username)
            device_token = row.token
            return device_token
        except DeviceToken.DoesNotExist:
            return None