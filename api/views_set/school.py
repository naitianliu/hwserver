from api.views_set.lib import *
from api.functions.school_helper import SchoolHelper


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def school_create(request):
    user_id = request.user.username
    req_data = json.loads(request.body)
    name = req_data['name']
    location_dict = req_data['location'] if 'location' in req_data else None
    address = req_data['address'] if 'address' in req_data else None
    SchoolHelper(user_id).create_new_school(name, location_dict=location_dict, address=address)
    res_data = dict(
        error=0
    )
    return Response(data=res_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def school_get_list(request):
    user_id = request.user.username
    schools = SchoolHelper(user_id).get_school_list()
    res_data = dict(
        error=0,
        schools=schools
    )
    return Response(data=res_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def school_update(request):
    user_id = request.user.username
    req_data = json.loads(request.body)
    school_uuid = req_data['uuid']
    name = req_data['name'] if 'name' in req_data else None
    location_dict = req_data['location'] if 'location' in req_data else None
    address = req_data['address'] if 'address' in req_data else None
    success = SchoolHelper(user_id).update_school_info(
        school_uuid,
        name=name,
        location_dict=location_dict,
        address=address)
    res_data = dict(
        error=success,
    )
    return Response(data=res_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def school_close(request):
    user_id = request.user.username
    req_data = json.loads(request.body)
    school_uuid = req_data['uuid']
    success = SchoolHelper(user_id).close_school(school_uuid)
    res_data = dict(
        error=success
    )
    return Response(data=res_data, status=status.HTTP_200_OK)