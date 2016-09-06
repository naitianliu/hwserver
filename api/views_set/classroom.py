from api.views_set.lib import *
from api.functions.classroom_helper import ClassroomHelper
from api.functions.update_helper import UpdateHelper


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def create(request):
    user_id = request.user.username
    req_data = json.loads(request.body)
    role = req_data['role']
    name = req_data['name']
    introduction = req_data['introduction']
    school_uuid = req_data['school_uuid']
    members = req_data['members'] if 'members' in req_data else None
    classroom_helper = ClassroomHelper(user_id, role)
    result_tup = classroom_helper.create_new_classroom(name, school_uuid, introduction, members=members)
    classroom_uuid = result_tup[0]
    classroom_code = result_tup[1]
    res_data = dict(
        error=0,
        classroom_uuid=classroom_uuid,
        classroom_code=classroom_code,
        timestamp=classroom_helper.timestamp_now
    )
    return Response(data=res_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def update(request):
    user_id = request.user.username
    req_data = json.loads(request.body)
    role = req_data['role']
    classroom_uuid = req_data['uuid']
    name = req_data['name'] if 'name' in req_data else None
    introduction = req_data['introduction'] if 'introduction' in req_data else None
    success = ClassroomHelper(user_id, role).update_classroom_info(classroom_uuid,
                                                                   name=name,
                                                                   introduction=introduction)
    res_data = dict(
        error=success
    )
    return Response(data=res_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def close(request):
    user_id = request.user.username
    req_data = json.loads(request.body)
    role = req_data['role']
    classroom_uuid = req_data['uuid']
    success = ClassroomHelper(user_id, role).close_classroom(classroom_uuid)
    res_data = dict(
        error=success
    )
    return Response(data=res_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def get_list(request):
    user_id = request.user.username
    role = request.GET['role']
    classrooms = ClassroomHelper(user_id, role).get_classroom_list()
    res_data = dict(
        error=0,
        classrooms=classrooms
    )
    return Response(data=res_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def search(request):
    user_id = request.user.username
    role = request.GET['role']
    keyword = request.GET['keyword']
    classrooms = ClassroomHelper(user_id, role).search_classrooms(keyword)
    res_data = dict(
        error=0,
        classrooms=classrooms
    )
    return Response(data=res_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def send_request_to_join(request):
    user_id = request.user.username
    req_data = json.loads(request.body)
    role = req_data['role']
    classroom_uuid = req_data['uuid']
    comment = req_data['comment'] if 'comment' in req_data else None
    classroom_helper = ClassroomHelper(user_id, role)
    request_uuid = classroom_helper.send_request_to_join(classroom_uuid, comment=comment)
    # update cache
    UpdateHelper(user_id, role, timestamp=classroom_helper.timestamp_now).new_pending_request(user_id,
                                                                                              classroom_uuid,
                                                                                              request_uuid)
    res_data = dict(
        error=0,
        request_uuid=request_uuid
    )
    return Response(data=res_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def approve_request(request):
    user_id = request.user.username
    req_data = json.loads(request.body)
    role = req_data['role']
    request_uuid = req_data['request_uuid']
    success = ClassroomHelper(user_id, role).approve_request(request_uuid)
    res_data = dict(
        error=success
    )
    return Response(data=res_data, status=status.HTTP_200_OK)