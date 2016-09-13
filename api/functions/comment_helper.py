from api.models import Comment
import json
import uuid
import datetime


class CommentHelper(object):
    def __init__(self, user_id, role):
        self.user_id = user_id
        self.role = role
        self.timestamp_now = int(datetime.datetime.now().strftime('%s'))

    def create(self, submission_uuid, info):
        comment_uuid = uuid.uuid1()
        Comment(
            uuid=comment_uuid,
            submission_uuid=submission_uuid,
            author=self.user_id,
            info=json.dumps(info),
            created_timestamp=self.timestamp_now
        ).save()
        return True, comment_uuid

    def get_list(self, submission_uuid):
        comments = []
        for row in Comment.objects.filter(submission_uuid=submission_uuid):
            comments.append(dict(
                comment_uuid=row.uuid,
                submission_uuid=row.submission_uuid,
                author=row.author,
                info=json.loads(row.info),
                created_timestamp=row.created_timestamp
            ))
        return comments

