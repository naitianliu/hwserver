from apns import APNs, Payload
from hwserver.settings import BASE_DIR
from user_auth.functions.device_token_helper import DeviceTokenHelper


class APNSHelper(object):
    def __init__(self, username):
        self.cert_path = BASE_DIR + '/support_files/certs/APNCert.pem'
        self.key_path = BASE_DIR + '/support_files/certs/APNKey.pem'
        self.device_token = DeviceTokenHelper(username).get_device_token()

    def send_simple_notification(self, message, payload_dict):
        if self.device_token:
            apns = APNs(use_sandbox=False, cert_file=self.cert_path, key_file=self.key_path)
            payload = Payload(alert=message, sound="default", badge=1, custom=payload_dict)
            apns.gateway_server.send_notification(self.device_token, payload)
            apns.gateway_server.register_response_listener(self.__response_listener)

    def __response_listener(self, error_response):
        print("client get error-response: " + str(error_response))