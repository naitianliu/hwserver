from ots2 import OTSClient, Condition
from hwserver.config import OTS
import uuid

"""
homework status:
'open', 'close'

"""


class HomeworkHelper(object):
    def __init__(self, user_id, role):
        self.ots_client = OTSClient(OTS['instance_endpoint'],
                                    OTS['access_key_id'],
                                    OTS['access_key_secret'],
                                    'homework',
                                    logger_name='table_store.log')
        self.user_id = user_id
        self.role = role
        self.homework_table = OTS['table']['homework']
        self.comment_table = OTS['table']['comment']
        self.student_submission_table = OTS['table']['student_submission']

    def create_new_homework(self, classroom_uuid, attrs):
        """teacher only"""
        homework_uuid = str(uuid.uuid1())
        status = 'open'
        primary_key = dict(
            homework_uuid=homework_uuid,
            classroom_uuid=classroom_uuid,
            status=status
        )
        attribute_columns = attrs
        condition = Condition('EXPECT_NOT_EXIST')
        try:
            self.ots_client.put_row(self.homework_table,
                                    condition=condition,
                                    primary_key=primary_key,
                                    attribute_columns=attribute_columns)
            return True, homework_uuid
        except Exception as err:
            print err
            return False, None

    def submit_homework(self, homework_uuid, attrs):
        """student only"""
        primary_key = dict(
            homework_uuid=homework_uuid,
            student_user_id=self.user_id
        )
        attribute_columns = attrs
        condition = Condition('EXPECT_NOT_EXIST')
        try:
            self.ots_client.put_row(self.student_submission_table,
                                    condition=condition,
                                    primary_key=primary_key,
                                    attribute_columns=attribute_columns)
            return True
        except Exception as err:
            print err
            return False

    def grade_homework(self, homework_uuid, student_user_id, score):
        """teacher only"""
        primary_key = dict(
            homework_uuid=homework_uuid,
            student_user_id=student_user_id
        )
        update_of_attribute_columns = dict(
            put=dict(score=score)
        )
        condition = Condition('EXPECT_EXIST')
        try:
            self.ots_client.update_row(self.student_submission_table,
                                       condition=condition,
                                       primary_key=primary_key,
                                       update_of_attribute_columns=update_of_attribute_columns)
            return True
        except Exception as err:
            print err
            return False

    def share_to_classroom(self):
        """teacher only"""
        pass

    def get_homework_list_by_classroom(self, classroom_uuid):
        """T & S"""
        pass

    def add_comment(self):
        """T & S"""
        pass

    def get_comment_list(self):
        """T & S"""
        pass










