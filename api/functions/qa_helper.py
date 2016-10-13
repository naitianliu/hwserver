from api.models import Question
from api.models import Answer
from django.db.models import F
from django.core.paginator import Paginator
from api.functions.classroom_helper import ClassroomHelper
from user_auth.functions.profile_helper import ProfileHelper
import uuid
import datetime


class QAHelper(object):
    def __init__(self, user_id, role, anonymous=False):
        self.user_id = user_id
        self.role = role
        self.anonymous = anonymous
        self.timestamp_now = int(datetime.datetime.now().strftime('%s'))
        self.classroom_helper = ClassroomHelper()
        self.classroom_name_dict = dict()
        self.profile_dict = dict()

    def create_question(self, classroom_uuid, content):
        question_uuid = uuid.uuid1()
        school_uuid = self.classroom_helper.get_school_uuid_by_classroom_uuid(classroom_uuid)
        Question(
            uuid=question_uuid,
            classroom_uuid=classroom_uuid,
            school_uuid=school_uuid,
            creator=self.user_id,
            role=self.role,
            anonymous=self.anonymous,
            active=True,
            answer_count=0,
            content=content,
            created_timestamp=self.timestamp_now,
            updated_timestamp=self.timestamp_now
        ).save()

    def close_question(self, question_uuid):
        try:
            row = Question.objects.get(uuid=question_uuid)
            creator = row.creator
            if creator == self.user_id:
                row.active = False
                row.save()
                success = True
            else:
                success = False
        except Question.DoesNotExist:
            success = False
        return success

    def create_answer(self, question_uuid, classroom_uuid, content):
        success = True
        answer_uuid = uuid.uuid1()
        Answer(
            uuid=answer_uuid,
            question_uuid=question_uuid,
            classroom_uuid=classroom_uuid,
            creator=self.user_id,
            role=self.role,
            anonymous=self.anonymous,
            content=content,
            agree_count=0,
            disagree_count=0,
            created_timestamp=self.timestamp_now,
        ).save()
        try:
            row = Question.objects.get(uuid=question_uuid)
            row.answer_count = F('answer_count') + 1
            row.updated_timestamp = self.timestamp_now
            row.save()
        except Question.DoesNotExist:
            success = False
        return success

    def agree_answer(self, answer_uuid):
        Answer.objects.filter(uuid=answer_uuid).update(agree_count=F('agree_count') + 1)

    def disagree_answer(self, answer_uuid):
        Answer.objects.filter(uuid=answer_uuid).update(disagree_count=F('disagree_count') + 1)

    def get_question_list(self, filter_type, page_number, school_uuid, per_page=20):
        questions = []
        if filter_type == 'new':
            p = Paginator(Question.objects.filter(active=True).order_by('-updated_timestamp'), per_page)
        elif filter_type == 'popular':
            p = Paginator(Question.objects.filter(active=True).order_by('-answer_count', '-updated_timestamp'), per_page)
        elif filter_type == 'me':
            p = Paginator(Question.objects.filter(active=True, creator=self.user_id).order_by('-updated_timestamp'), per_page)
        else:
            p = Paginator(Question.objects.filter(active=True).order_by('-updated_timestamp'), per_page)
        num_pages = p.num_pages
        if page_number <= num_pages:
            page_objects = p.page(page_number).object_list
            for row in page_objects:
                classroom_uuid = row.classroom_uuid
                classroom_name = self.__get_classroom_name(classroom_uuid)
                anonymous = row.anonymous
                creator = row.creator
                profile = self.__get_profile(creator, anonymous)
                nickname = profile['nickname'] if profile else None
                img_url = profile['img_url'] if profile else None
                questions.append(dict(
                    question_uuid=row.uuid,
                    classroom_uuid=classroom_uuid,
                    classroom_name=classroom_name,
                    school_uuid=school_uuid,
                    creator=creator,
                    nickname=nickname,
                    img_url=img_url,
                    role=row.role,
                    anonymous=anonymous,
                    answer_count=row.answer_count,
                    content=row.content,
                    created_timestamp=row.created_timestamp,
                    updated_timestamp=row.updated_timestamp
                ))
        return questions

    def get_answer_list(self, question_uuid, page_number, per_page=20):
        answers = []
        p = Paginator(Answer.objects.filter(question_uuid=question_uuid)
                      .order_by('-agree_count', '-created_timestamp'), per_page)
        num_pages = p.num_pages
        if page_number <= num_pages:
            page_objects = p.page(page_number).object_list
            for row in page_objects:
                classroom_uuid = row.classroom_uuid
                classroom_name = self.__get_classroom_name(classroom_uuid)
                anonymous = row.anonymous
                creator = row.creator
                profile = self.__get_profile(creator, anonymous)
                nickname = profile['nickname'] if profile else None
                img_url = profile['img_url'] if profile else None
                answers.append(dict(
                    answer_uuid=row.uuid,
                    question_uuid=row.question_uuid,
                    classroom_uuid=classroom_uuid,
                    classroom_name=classroom_name,
                    creator=creator,
                    nickname=nickname,
                    img_url=img_url,
                    role=row.role,
                    anonymous=anonymous,
                    content=row.content,
                    agree_count=row.agree_count,
                    disagree_count=row.disagree_count,
                    created_timestamp=row.created_timestamp
                ))
        return answers

    def __get_classroom_name(self, classroom_uuid):
        if classroom_uuid in self.classroom_name_dict:
            classroom_name = self.classroom_name_dict[classroom_uuid]
        else:
            classroom_name = self.classroom_helper.get_classroom_name_by_uuid(classroom_uuid)
            self.classroom_name_dict[classroom_uuid] = classroom_name
        return classroom_name

    def __get_profile(self, user_id, anonymous):
        if anonymous:
            profile = None
        elif user_id in self.profile_dict:
            profile = self.profile_dict[user_id]
        else:
            profile = ProfileHelper(user_id).get_profile()
            self.profile_dict[user_id] = profile
        return profile
