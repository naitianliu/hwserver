from api.models import Classroom
from api.models import ClassroomMember
from api.models import JoinClassroomRequest
from api.functions.school_helper import SchoolHelper
from user_auth.functions.profile_helper import ProfileHelper
import uuid
import datetime


class ClassroomHelper(object):
    def __init__(self, user_id=None, role=None):
        self.user_id = user_id
        self.timestamp_now = int(datetime.datetime.now().strftime('%s'))
        self.role = role

    def create_new_classroom(self, name, school_uuid, introduction, members=None):
        """teacher only"""
        """
        members example:
        [{
            "role": "t",
            "user_id": "****"
        }]
        """
        classroom_uuid = uuid.uuid1()
        code = self.__generate_code_string()
        Classroom(
            uuid=classroom_uuid,
            name=name,
            introduction=introduction,
            creator=self.user_id,
            school_uuid=school_uuid,
            code=code,
            active=True,
            created_timestamp=self.timestamp_now,
            updated_timestamp=self.timestamp_now
        ).save()
        creator_info = {"user_id": self.user_id, "role": "t"}
        if not members:
            members = [creator_info]
        else:
            if creator_info not in members:
                members.append(creator_info)
        self.__add_members(classroom_uuid, members)
        return classroom_uuid, code

    def update_classroom_info(self, classroom_uuid, name=None, introduction=None, members=None):
        """teacher only"""
        try:
            row = Classroom.objects.get(uuid=classroom_uuid)
            if name or members or introduction:
                row.updated_timestamp = self.timestamp_now
            if name:
                row.name = name
                row.save()
            if introduction:
                row.introduction = introduction
                row.save()
            if members:
                self.__add_members(classroom_uuid, members)
            return True
        except Classroom.DoesNotExist:
            return False

    def close_classroom(self, classroom_uuid):
        """teacher only"""
        try:
            row = Classroom.objects.get(uuid=classroom_uuid)
            if row.creator == self.user_id:
                row.active = False
                row.updated_timestamp = self.timestamp_now
                row.save()
                return True
            else:
                return False
        except Classroom.DoesNotExist:
            return False

    def close_classrooms_by_school(self, school_uuid):
        for row in Classroom.objects.filter(school_uuid=school_uuid, active=True):
            row.active = False
            row.updated_timestamp = self.timestamp_now
            row.save()

    def get_classroom_list(self):
        """T & S"""
        classroom_uuid_list = self.__get_classroom_uuid_list()
        classrooms = self.__get_classroom_info_list_by_uuid_list(classroom_uuid_list)
        return classrooms

    def get_classroom_info(self, classroom_uuid):
        classrooms = self.__get_classroom_info_list_by_uuid_list([classroom_uuid])
        if classrooms:
            return classrooms[0]
        else:
            return None

    def get_school_uuid_by_classroom_uuid(self, classroom_uuid):
        try:
            row = Classroom.objects.get(uuid=classroom_uuid)
            school_uuid = row.school_uuid
            return school_uuid
        except Classroom.DoesNotExist:
            return None

    def get_classroom_name_by_uuid(self, classroom_uuid):
        try:
            row = Classroom.objects.get(uuid=classroom_uuid)
            classroom_name = row.name
            return classroom_name
        except Classroom.DoesNotExist:
            return None

    def invite_people_to_join_classroom(self):
        """teacher only"""
        pass

    def generate_classroom_qrcode(self):
        """teacher only"""
        pass

    def send_request_to_join(self, classroom_uuid, comment=None):
        """T & S"""

        rows = JoinClassroomRequest.objects.filter(classroom_uuid=classroom_uuid,
                                                   requester=self.user_id,
                                                   role=self.role,
                                                   status="pending")
        if len(rows) == 0:
            request_uuid = uuid.uuid1()
            JoinClassroomRequest(
                uuid=request_uuid,
                classroom_uuid=classroom_uuid,
                requester=self.user_id,
                role=self.role,
                comment=comment,
                status="pending",
                created_timestamp=self.timestamp_now,
                updated_timestamp=self.timestamp_now
            ).save()
        else:
            item = rows[0]
            request_uuid = item.uuid
        return request_uuid

    def approve_request(self, request_uuid):
        """teacher only"""
        try:
            row = JoinClassroomRequest.objects.get(uuid=request_uuid)
            requester = row.requester
            row.status = "approved"
            row.approver = self.user_id
            row.updated_timestamp = self.timestamp_now
            row.save()
            classroom_uuid = row.classroom_uuid
            role = row.role
            requester_user_id = row.requester
            member_info = dict(
                role=role,
                user_id=requester_user_id
            )
            members = self.__get_members_by_classroom(classroom_uuid)
            if member_info not in members:
                members.append(member_info)
            self.__add_members(classroom_uuid, members)
            return True, requester, role, classroom_uuid
        except JoinClassroomRequest.DoesNotExist:
            return False, None, None, None

    def get_pending_requests(self):
        classroom_uuid_list = self.__get_classroom_uuid_list()
        pending_requests = []
        for row in JoinClassroomRequest.objects.filter(classroom_uuid__in=classroom_uuid_list, status="pending"):
            pending_requests.append(dict(
                request_uuid=row.uuid,
                classroom_uuid=row.classroom_uuid,
                requester=row.requester,
                role=row.role,
                comment=row.comment,
                status=row.status,
                created_timestamp=row.created_timestamp,
                updated_timestamp=row.updated_timestamp
            ))
        return pending_requests

    def input_invitation_code_to_join(self):
        """T & S"""
        pass

    def scan_classroom_qrcode_to_join(self):
        """T & S"""
        pass

    def search_classrooms(self, keyword):
        """T & S"""
        keyword = keyword.strip()
        classroom_uuid_list = []
        for row in Classroom.objects.filter(code=keyword):
            classroom_uuid_list.append(row.uuid)
        classrooms = self.__get_classroom_info_list_by_uuid_list(classroom_uuid_list)
        return classrooms

    def __get_classroom_uuid_list(self):
        classroom_uuid_list = []
        for row in ClassroomMember.objects.filter(user_id=self.user_id, role=self.role, active=True):
            classroom_uuid = row.classroom_uuid
            classroom_uuid_list.append(classroom_uuid)
        return classroom_uuid_list

    def __get_classroom_info_list_by_uuid_list(self, classroom_uuid_list):
        classrooms = []
        members_dict = self.__get_members_dict(classroom_uuid_list)
        school_helper = SchoolHelper(self.user_id)
        for row in Classroom.objects.filter(uuid__in=classroom_uuid_list, active=True):
            classroom_uuid = row.uuid
            school_uuid = row.school_uuid
            school_info = school_helper.get_school_info_by_uuid(school_uuid)
            classrooms.append(dict(
                classroom_uuid=classroom_uuid,
                classroom_name=row.name,
                introduction=row.introduction,
                creator=row.creator,
                active=row.active,
                school_uuid=school_uuid,
                school_info=school_info,
                code=row.code,
                created_timestamp=row.created_timestamp,
                updated_timestamp=row.updated_timestamp,
                members=members_dict[classroom_uuid] if classroom_uuid in members_dict else []
            ))
        return classrooms

    def __get_members_dict(self, classroom_uuid_list):
        members_dict = dict()
        for row in ClassroomMember.objects.filter(classroom_uuid__in=classroom_uuid_list, active=True):
            classroom_uuid = row.classroom_uuid
            if classroom_uuid not in members_dict:
                members_dict[classroom_uuid] = []
            role = row.role
            member_user_id = row.user_id
            members_dict[classroom_uuid].append(dict(
                role=role,
                user_id=member_user_id,
                profile=ProfileHelper(member_user_id).get_profile()
            ))
        return members_dict

    def get_members(self, classroom_uuid):
        members = self.__get_members_by_classroom(classroom_uuid=classroom_uuid)
        return members

    def __get_members_by_classroom(self, classroom_uuid):
        members = []
        for row in ClassroomMember.objects.filter(classroom_uuid=classroom_uuid, active=True):
            members.append(dict(
                role=row.role,
                user_id=row.user_id
            ))
        return members

    def __add_members(self, classroom_uuid, members):
        old_members = self.__get_members_by_classroom(classroom_uuid)
        print old_members
        print members
        for member in members:
            role = member['role']
            user_id = member['user_id']
            rows = ClassroomMember.objects.filter(classroom_uuid=classroom_uuid,
                                                  user_id=user_id,
                                                  role=role)
            if len(rows) > 0:
                for row in rows:
                    if not row.active:
                        row.active = True
                        row.updated_timestamp = self.timestamp_now
                        row.save()
            else:
                ClassroomMember(
                    classroom_uuid=classroom_uuid,
                    user_id=user_id,
                    role=role,
                    active=True,
                    created_timestamp=self.timestamp_now,
                    updated_timestamp=self.timestamp_now
                ).save()
        for old_member in old_members:
            print 123
            if old_member not in members:
                role = old_member['role']
                user_id = old_member['user_id']
                rows = ClassroomMember.objects.filter(classroom_uuid=classroom_uuid, user_id=user_id, role=role, active=True)
                for row in rows:
                    row.active = False
                    row.save()

    def __generate_code_string(self):
        base_number = 1119
        length = Classroom.objects.all().count()
        code = base_number + length + 10
        return str(code)

    def get_creator_by_classroom(self, classroom_uuid):
        try:
            row = Classroom.objects.get(uuid=classroom_uuid)
            creator = row.creator
            return creator
        except Classroom.DoesNotExist:
            return None