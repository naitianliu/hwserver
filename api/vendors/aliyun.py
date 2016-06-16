from aliyunsdkcore import client
from aliyunsdksts.request.v20150401 import AssumeRoleRequest
from hwserver import config
import json


class AliyunHelper(object):
    def __init__(self):
        self.access_key_id = config.VENDORS['aliyun']['access_key_id']
        self.access_key_secret = config.VENDORS['aliyun']['access_key_secret']
        self.role_arn = config.VENDORS['aliyun']['assume_role']['role_arn']
        self.role_session_name = config.VENDORS['aliyun']['assume_role']['role_session_name']
        self.duration_seconds = config.VENDORS['aliyun']['assume_role']['duration_seconds']
        self.region = config.VENDORS['aliyun']['region']

    def get_sts_token(self):
        clt = client.AcsClient(self.access_key_id, self.access_key_secret, self.region)
        request = AssumeRoleRequest.AssumeRoleRequest()
        request.set_accept_format('json')
        request.set_RoleArn(self.role_arn)
        request.set_RoleSessionName(self.role_session_name)
        request.set_DurationSeconds(self.duration_seconds)
        response = clt.do_action(request)
        res_dict = json.loads(response)
        credentials = res_dict['Credentials']
        return credentials


