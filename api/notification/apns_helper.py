from apns import APNs, Payload
from hwserver.settings import BASE_DIR
from hwserver.settings import PROD
from user_auth.functions.device_token_helper import DeviceTokenHelper


class APNSHelper(object):
    def __init__(self, username):
        self.cert_path = BASE_DIR + '/support_files/certs/APNCert.pem'
        self.key_path = BASE_DIR + '/support_files/certs/APNKey.pem'
        self.device_token = DeviceTokenHelper(username).get_device_token()

    def send_simple_notification(self, message):
        if self.device_token:
            print self.device_token
            apns = APNs(use_sandbox=not PROD, cert_file=self.cert_path, key_file=self.key_path)
            payload = Payload(alert=message, sound="default", badge=1)
            apns.gateway_server.send_notification(self.device_token, payload)
            apns.gateway_server.register_response_listener(self.__response_listener)

    def __response_listener(self, error_response):
        print("client get error-response: " + str(error_response))