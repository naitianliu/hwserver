from hwserver.settings import PROD

if PROD:
    OTS_INSTANCE_ENDPOINT = 'http://homework.cn-shanghai.ots-internal.aliyuncs.com'
else:
    OTS_INSTANCE_ENDPOINT = 'http://homework.cn-shanghai.ots.aliyuncs.com'


VENDORS = {
    'aliyun': {
        'access_key_id': '4xKKGizrR0bBXp7U',
        'access_key_secret': 'UxeRGWFo0PZp2DBfREWULta8HWVQEE',
        'assume_role': {
            'role_arn': 'acs:ram::1342940224067286:role/aliyunosstokengeneratorrole',
            'role_session_name': 'external-username',
            'duration_seconds': 3600,
        },
        'region': 'cn-hangzhou'
    },
    'alidayu': {
        'url': 'http://gw.api.taobao.com/router/rest',
        'sms_type': 'normal',
        'sms_free_sign_name': '\xE7\xAA\x97\xE5\xA4\x96',
        'sms_template_code': 'SMS_10880721',
        'app_key': '23391266',
        'app_secret': '07a28ef99101a18e06efdc8532d12ec4',
    },
}

OTS = {
    'access_key_id': 'HePLlPUE2bQze4T2',
    'access_key_secret': 'uAQ2p83daghEMALd042nl4MYlhPHFT',
    'instance_endpoint': OTS_INSTANCE_ENDPOINT,
    'table': {
        'homework': 'homework_table',
        'comment': 'comment_table',
        'student_submission': 'student_submission_table'
    }
}