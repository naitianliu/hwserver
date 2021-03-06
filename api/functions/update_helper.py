from django.core.cache import cache
from user_auth.functions.profile_helper import ProfileHelper
from api.functions.classroom_helper import ClassroomHelper
from api.functions.homework_helper import HomeworkHelper
from api.notification.message_template import MESSAGE
from api.async import tasks
import datetime

UPDATE_KEY_TYPES = {
    'requests': 'requests',
    'approvals': 'approvals',
    'submissions': 'submissions',
    'members': 'members',
    'classrooms': 'classrooms',
    'homeworks': 'homeworks',
    'grades': 'grades',
    'comments': 'comments'
}
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
            requester_role=self.role,
            timestamp=self.timestamp
        )
        key = self.__get_key(creator_user_id, 't', UPDATE_KEY_TYPES['requests'])
        self.__update_value(key, item_dict)
        # send message
        message = MESSAGE['requests'].format(requester_profile_info['nickname'])
        tasks.send_apns_notification.delay(creator_user_id, message)

    def request_approved(self, requester_user_id, requester_role, classroom_uuid):
        """T & S"""
        approver = self.user_id
        approver_profile_info = ProfileHelper(approver).get_profile()
        classroom_info = ClassroomHelper(user_id=requester_user_id, role=requester_role).get_classroom_info(classroom_uuid)
        item_dict = dict(
            approver_profile_info=approver_profile_info,
            classroom_info=classroom_info,
            timestamp=self.timestamp
        )
        key = self.__get_key(requester_user_id, requester_role, UPDATE_KEY_TYPES['approvals'])
        self.__update_value(key, item_dict)
        # send message
        classroom_name = classroom_info['classroom_name'] if 'classroom_name' in classroom_info else ""
        message = MESSAGE['approvals'].format(classroom_name)
        tasks.send_apns_notification.delay(requester_user_id, message)

    def member_added_into_classroom(self, profile_info, classroom_info=None):
        """T & S"""
        pass

    def new_submission(self, student_user_id, homework_uuid):
        """Teacher only"""
        student_nickname = ProfileHelper(student_user_id).get_nickname_by_username(student_user_id)
        creator = HomeworkHelper().get_creator_by_homework_uuid(homework_uuid)
        item_dict = dict(
            student_user_id=student_user_id,
            student_nickname=student_nickname,
            homework_uuid=homework_uuid,
            timestamp=self.timestamp
        )
        key = self.__get_key(creator, 't', UPDATE_KEY_TYPES['submissions'])
        self.__update_value(key, item_dict)
        # send message
        message = MESSAGE['submissions']
        tasks.send_apns_notification.delay(creator, message)

    def new_comment(self, author_user_id, receiver_user_id, receiver_role, homework_uuid, submission_uuid, info):
        """T & S"""
        author_profile_info = ProfileHelper(author_user_id).get_profile()
        item_dict = dict(
            author_profile_info=author_profile_info,
            homework_uuid=homework_uuid,
            submission_uuid=submission_uuid,
            info=info,
            timestamp=self.timestamp
        )
        key = self.__get_key(receiver_user_id, receiver_role, UPDATE_KEY_TYPES['comments'])
        self.__update_value(key, item_dict)
        # send message
        nickname = author_profile_info['nickname'] if author_profile_info else ""
        message = MESSAGE['comments'].format(nickname)
        tasks.send_apns_notification.delay(receiver_user_id, message)

    def submission_graded(self, submission_uuid, score):
        """Student Only"""
        submitter = HomeworkHelper().get_submitter_by_submission_uuid(submission_uuid)
        item_dict = dict(
            submission_uuid=submission_uuid,
            score=score,
            timestamp=self.timestamp
        )
        key = self.__get_key(submitter, 's', UPDATE_KEY_TYPES['grades'])
        self.__update_value(key, item_dict)
        # send message
        message = MESSAGE['grades']
        tasks.send_apns_notification.delay(submitter, message)

    def new_homework(self, classroom_uuid):
        """T & S"""
        classroom_helper = ClassroomHelper()
        members = classroom_helper.get_members(classroom_uuid)
        classroom_name = classroom_helper.get_classroom_name_by_uuid(classroom_uuid)
        item_dict = dict(
            classroom_uuid=classroom_uuid,
            classroom_name=classroom_name,
            timestamp=self.timestamp
        )
        for member in members:
            user_id = member['user_id']
            role = member['role']
            key = self.__get_key(user_id, role, UPDATE_KEY_TYPES['homeworks'])
            self.__update_value(key, item_dict)
            # send message
            message = MESSAGE['homeworks']
            tasks.send_apns_notification.delay(user_id, message)

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

    def __update_value(self, key, item_dict):
        current_values = self.__read_from_cache(key)
        if current_values:
            current_values.append(item_dict)
        else:
            current_values = [item_dict]
        self.__write_to_cache(key, current_values)

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
