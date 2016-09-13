from random import randint
from django.core.cache import cache


KEY = "invitation_code"
REDIS_TIMEOUT = 7*24*60*60


class InvitationHelper(object):
    def __init__(self):
        pass

    def generate_invitation_code(self):
        code = randint(100000, 999999)
        code = str(code)
        code_list = self.__read_from_cache(KEY)
        if code_list:
            code_list.append(code)
        else:
            code_list = [code]
        self.__write_to_cache(key=KEY, value=code_list)
        return code

    def validate_invitation_code(self, code_str):
        code_list = self.__read_from_cache(KEY)
        result = code_str in code_list
        if result:
            for i in range(len(code_list)):
                if code_str == code_list[i]:
                    code_list.pop(i)
                    self.__write_to_cache(KEY, code_list)
                    break
        return result

    def __read_from_cache(self, key):
        value = cache.get(key)
        return value

    def __write_to_cache(self, key, value):
        cache.set(key, value, REDIS_TIMEOUT)