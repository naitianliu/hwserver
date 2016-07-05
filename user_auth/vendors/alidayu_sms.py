from user_auth.vendors import top
from hwserver.config import VENDORS


class SMSHelper(object):
    def __init__(self):
        self.sms_type = VENDORS['alidayu']['sms_type']
        self.sms_free_sign_name = VENDORS['alidayu']['sms_free_sign_name']
        self.sms_template_code = VENDORS['alidayu']['sms_template_code']
        self.app_key = VENDORS['alidayu']['app_key']
        self.app_secret = VENDORS['alidayu']['app_secret']
        print self.sms_free_sign_name

    def send_code_via_sms(self, phone_number, code):
        req = top.api.AlibabaAliqinFcSmsNumSendRequest()
        req.set_app_info(top.appinfo(self.app_key, self.app_secret))
        req.extend = ""
        req.sms_type = self.sms_type
        req.sms_free_sign_name = self.sms_free_sign_name
        req.sms_param = "{name:'%s'}" % code
        req.rec_num = phone_number
        req.sms_template_code = self.sms_template_code
        try:
            resp = req.getResponse()
            print (resp)
        except Exception, e:
            print (e)