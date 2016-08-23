from api.views_set.lib import *
from api.functions.homework_helper import HomeworkHelper


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def create(request):
    user_id = request.user.username
    req_data = json.loads(request.body)
    role = req_data['role']
    classroom_uuid = req_data['classroom_uuid']
    attrs = req_data['attrs']
    result_tup = HomeworkHelper(user_id, role).create_new_homework(classroom_uuid, attrs)
    success = result_tup[0]
    homework_uuid = result_tup[1]
    res_data = dict(
        success=success,
        homework_uuid=homework_uuid
    )
    return Response(data=res_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def submit(request):
    user_id = request.user.username
    req_data = json.loads(request.body)
    role = req_data['role']
    homework_uuid = req_data['homework_uuid']
    attrs = req_data['attrs']
    success = HomeworkHelper(user_id, role).submit_homework(homework_uuid, attrs)
    res_data = dict(
        success=success
    )
    return Response(data=res_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def grade(request):
    user_id = request.user.username
    req_data = json.loads(request.body)
    role = req_data['role']
    homework_uuid = req_data['homework_uuid']
    student_user_id = req_data['student_user_id']
    score = req_data['score']
    success = HomeworkHelper(user_id, role).grade_homework(homework_uuid, student_user_id, score)
    res_data = dict(
        success=success
    )
    return Response(data=res_data, status=status.HTTP_200_OK)