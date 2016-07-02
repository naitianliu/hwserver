# coding=utf-8
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
        'sms_free_sign_name': '窗外',
        'sms_template_code': 'SMS_10880721',
        'app_key': '23391266',
        'app_secret': '07a28ef99101a18e06efdc8532d12ec4',
    }
}