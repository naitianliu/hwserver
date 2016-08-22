from api.models import School
import uuid
import datetime


class SchoolHelper(object):
    def __init__(self, user_id):
        self.user_id = user_id
        self.time_now = datetime.datetime.now()

    def create_new_school(self, name, location_dict=None, address=None):
        school_uuid = uuid.uuid1()
        location_x = location_dict['x'] if location_dict else None
        location_y = location_dict['y'] if location_dict else None
        School(
            uuid=school_uuid,
            name=name,
            creator=self.user_id,
            location_x=location_x,
            location_y=location_y,
            address=address,
            active=True,
            created_time=self.time_now,
            last_updated_time=self.time_now
        ).save()

    def get_school_list(self):
        schools = []
        for row in School.objects.filter(creator=self.user_id, active=True):
            schools.append(dict(
                uuid=row.uuid,
                name=row.name,
                creator=row.creator,
                location_x=row.location_x,
                location_y=row.location_y,
                address=row.address,
                active=row.active,
                created_time=row.created_time,
                last_updated_time=row.last_updated_time
            ))
        return schools

    def update_school_info(self, school_uuid, name=None, location_dict=None, address=None):
        try:
            row = School.objects.get(uuid=school_uuid)
            if name:
                row.name = name
            if location_dict:
                location_x = location_dict['x']
                location_y = location_dict['y']
                row.location_x = location_x
                row.location_y = location_y
            if address:
                row.address = address
            row.last_updated_time = self.time_now
            row.save()
            return True
        except School.DoesNotExist:
            return False

    def close_school(self, school_uuid):
        try:
            row = School.objects.get(uuid=school_uuid)
            row.active = False
            row.last_updated_time = self.time_now
            row.save()
            return True
        except School.DoesNotExist:
            return False
