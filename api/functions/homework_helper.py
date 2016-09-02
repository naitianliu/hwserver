from api.models import Homework
from api.models import Submission
import uuid
import json
import datetime


class HomeworkHelper(object):
    def __init__(self, user_id, role):
        self.user_id = user_id
        self.role = role
        self.timestamp_now = int(datetime.datetime.now().strftime('%s'))

    def create_new_homework(self, classroom_uuid, info):
        """teacher only"""
        homework_uuid = uuid.uuid1()
        Homework(
            uuid=homework_uuid,
            classroom_uuid=classroom_uuid,
            creator=self.user_id,
            active=True,
            info=json.dumps(info),
            created_timestamp=self.timestamp_now,
            updated_timestamp=self.timestamp_now
        ).save()
        return True, homework_uuid

    def submit_homework(self, homework_uuid, info):
        """
        student only
        submission status: 0: initial
        """
        submission_uuid = uuid.uuid1()
        Submission(
            uuid=submission_uuid,
            homework_uuid=homework_uuid,
            user_id=self.user_id,
            score=None,
            status="0",
            info=json.dumps(info),
            created_timestamp=self.timestamp_now,
            updated_timestamp=self.timestamp_now
        ).save()
        return True, submission_uuid

    def grade_homework(self, submission_uuid, score):
        """teacher only"""
        try:
            row = Submission.objects.get(uuid=submission_uuid)
            row.score = score
            row.save()
            return True
        except Submission.DoesNotExist:
            return False

    def close_homework(self, homework_uuid):
        """teacher only"""
        try:
            row = Homework.objects.get(uuid=homework_uuid)
            row.active = False
            row.save()
            return True
        except Homework.DoesNotExist:
            return False

    def get_homework_list_by_classroom(self, classroom_uuid):
        """T & S"""
        homework_list = []
        for row in Homework.objects.filter(classroom_uuid=classroom_uuid, active=True):
            homework_list.append(dict(
                uuid=row.uuid,
                classroom_uuid=row.classroom_uuid,
                creator=row.creator,
                active=row.active,
                info=json.loads(row.info),
                created_timestamp=row.created_timestamp,
                updated_timestamp=row.updated_timestamp
            ))
        return homework_list

    def get_submission_list_by_homework(self, homework_uuid):
        submission_list = []
        for row in Submission.objects.filter(homework_uuid=homework_uuid):
            submission_list.append(dict(
                uuid=row.uuid,
                homework_uuid=row.homework_uuid,
                user_id=row.user_id,
                score=row.score,
                status=row.status,
                info=json.loads(row.info),
                created_timestamp=row.created_timestamp,
                updated_timestamp=row.updated_timestamp
            ))
        return submission_list











