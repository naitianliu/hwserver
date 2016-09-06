from django.core.cache import cache
from user_auth.functions.profile_helper import ProfileHelper
from api.functions.classroom_helper import ClassroomHelper
import datetime

UPDATE_KEY_TYPES = ['requests', 'submissions', 'members', 'classrooms', 'homeworks']
REDIS_TIMEOUT = 7*24*60*60


class UpdateHelper(object):
    def __init__(self, user_id, role, timestamp=None):
        self.user_id = user_id
        self.role = role
        if timestamp:
            self.timestamp = timestamp
        else:
            self.timestamp = int(datetime.datetime.now().strftime('%s'))

    def new_pending_request(self, requester, classroom_uuid, request_uuid):
        """T & S"""
        creator_user_id = ClassroomHelper().get_creator_by_classroom(classroom_uuid)
        requester_profile_info = ProfileHelper(requester).get_profile()
        item_dict = dict(
            requester_profile=requester_profile_info,
            classroom_uuid=classroom_uuid,
            request_uuid=request_uuid,
            timestamp=self.timestamp
        )
        key = self.__get_key(creator_user_id, 't', UPDATE_KEY_TYPES[0])
        print key
        current_requests = self.__read_from_cache(key)
        if current_requests:
            current_requests.append(item_dict)
        else:
            current_requests = [item_dict]
        self.__write_to_cache(key, current_requests)

    def request_approval(self, profile_info, approver):
        """T & S"""
        pass

    def member_added_into_classroom(self, profile_info, classroom_info=None):
        """T & S"""
        pass

    def new_submission(self, student_user_id, submission_info):
        """Teacher only"""
        pass

    def submission_graded(self):
        """Student Only"""
        pass

    def new_homework(self):
        """T & S"""
        pass

    def get_all_updates(self):
        """T & S"""
        updates = dict()
        for key_type in UPDATE_KEY_TYPES:
            key = self.__get_key(self.user_id, self.role, key_type)
            value = self.__read_from_cache(key)
            if not value:
                value = []
            updates[key_type] = value
            self.__delete_from_cache(key)
        return updates

    def __read_from_cache(self, key):
        value = cache.get(key)
        return value

    def __write_to_cache(self, key, value):
        cache.set(key, value, REDIS_TIMEOUT)

    def __delete_from_cache(self, key):
        cache.delete(key)

    def __get_key(self, user_id, role, key_type):
        key = "%s_%s_%s" % (user_id, role, key_type)
        return key
