from api.models import Classroom
from api.models import ClassroomMember
from api.models import JoinClassroomRequest
from api.functions.school_helper import SchoolHelper
import uuid
import datetime


class ClassroomHelper(object):
    def __init__(self, user_id, role):
        self.user_id = user_id
        self.time_now = datetime.datetime.now()
        self.role = role

    def create_new_classroom(self, name, school_uuid, members=None):
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
            creator=self.user_id,
            school_uuid=school_uuid,
            code=code,
            active=True,
            created_time=self.time_now,
            last_updated_time=self.time_now
        ).save()
        if members:
            self.__add_members(classroom_uuid, members)
        return code

    def update_classroom_info(self, classroom_uuid, name=None, members=None):
        """teacher only"""
        try:
            row = Classroom.objects.get(uuid=classroom_uuid)
            if name:
                row.name = name
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
                row.last_updated_time = self.time_now
                row.save()
                return True
            else:
                return False
        except Classroom.DoesNotExist:
            return False

    def get_classroom_list(self):
        """T & S"""
        classroom_uuid_list = self.__get_classroom_uuid_list()
        classrooms = self.__get_classroom_info_list_by_uuid_list(classroom_uuid_list)
        return classrooms

    def invite_people_to_join_classroom(self):
        """teacher only"""
        pass

    def generate_classroom_qrcode(self):
        """teacher only"""
        pass

    def send_request_to_join(self, classroom_uuid, comment=None):
        """T & S"""
        request_uuid = uuid.uuid1()
        rows = JoinClassroomRequest.objects.filter(classroom_uuid=classroom_uuid,
                                                   requester=self.user_id,
                                                   role=self.role,
                                                   status="pending")
        if len(rows) == 0:
            JoinClassroomRequest(
                uuid=request_uuid,
                classroom_uuid=classroom_uuid,
                requester=self.user_id,
                role=self.role,
                comment=comment,
                status="pending",
                created_time=self.time_now,
                last_updated_time=self.time_now
            ).save()
        return request_uuid

    def approve_request(self, request_uuid):
        """teacher only"""
        try:
            row = JoinClassroomRequest.objects.get(uuid=request_uuid)
            row.status = "approved"
            row.approver = self.user_id
            row.last_updated_time = self.time_now
            row.save()
            classroom_uuid = row.classroom_uuid
            role = row.role
            requester_user_id = row.requester
            members = [dict(
                role=role,
                user_id=requester_user_id
            )]
            self.__add_members(classroom_uuid, members)
            return True
        except JoinClassroomRequest.DoesNotExist:
            return False

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
                created_time=row.created_time,
                last_updated_time=row.last_updated_time
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
        for row in Classroom.objects.filter(uuid__in=classroom_uuid_list, active=True):
            classroom_uuid = row.uuid
            classrooms.append(dict(
                classroom_uuid=classroom_uuid,
                name=row.name,
                creator=row.creator,
                school_uuid=row.school_uuid,
                code=row.code,
                created_time=row.created_time,
                last_updated_time=row.last_updated_time,
                members=members_dict[classroom_uuid]
            ))
        return classrooms

    def __get_members_dict(self, classroom_uuid_list):
        members_dict = dict()
        for row in ClassroomMember.objects.filter(classroom_uuid__in=classroom_uuid_list, active=True):
            classroom_uuid = row.classroom_uuid
            if classroom_uuid not in members_dict:
                members_dict[classroom_uuid] = []
            role = row.role
            members_dict[classroom_uuid].append(dict(
                role=role,
                user_id=row.user_id
            ))
        return members_dict

    def __add_members(self, classroom_uuid, members):
        print members
        for member in members:
            role = member['role']
            user_id = member['user_id']
            try:
                row = ClassroomMember.objects.get(classroom_uuid=classroom_uuid,
                                                  user_id=user_id,
                                                  role=role)
                if not row.active:
                    row.active = True
                    row.last_updated_time = self.time_now
                    row.save()
            except ClassroomMember.DoesNotExist:
                ClassroomMember(
                    classroom_uuid=classroom_uuid,
                    user_id=user_id,
                    role=role,
                    active=True,
                    created_time=self.time_now,
                    last_updated_time=self.time_now
                ).save()

    def __generate_code_string(self):
        base_number = 1119
        length = Classroom.objects.all().count()
        code = base_number + length + 10
        return str(code)