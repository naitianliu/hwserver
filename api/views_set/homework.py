from api.views_set.lib import *
from api.functions.homework_helper import HomeworkHelper
from api.functions.comment_helper import CommentHelper
from api.functions.update_helper import UpdateHelper


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def create(request):
    user_id = request.user.username
    req_data = json.loads(request.body)
    role = req_data['role']
    classroom_uuid = req_data['classroom_uuid']
    attrs = req_data['info']
    homework_helper = HomeworkHelper(user_id, role)
    result_tup = homework_helper.create_new_homework(classroom_uuid, attrs)
    success = result_tup[0]
    homework_uuid = result_tup[1]
    timestamp = homework_helper.timestamp_now
    # update notification queue
    if success:
        UpdateHelper(user_id, role, timestamp=timestamp).new_homework(classroom_uuid)
    res_data = dict(
        success=success,
        homework_uuid=homework_uuid,
        timestamp=timestamp
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
    attrs = req_data['info']
    homework_helper = HomeworkHelper(user_id, role)
    result_tup = homework_helper.submit_homework(homework_uuid, attrs)
    success = result_tup[0]
    submission_uuid = result_tup[1]
    timestamp = homework_helper.timestamp_now
    # update
    if success:
        UpdateHelper(user_id, role, timestamp=timestamp).new_submission(user_id, homework_uuid)
    res_data = dict(
        success=success,
        submission_uuid=submission_uuid,
        timestamp=timestamp
    )
    return Response(data=res_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def grade(request):
    user_id = request.user.username
    req_data = json.loads(request.body)
    role = req_data['role']
    submission_uuid = req_data['submission_uuid']
    score = req_data['score']
    homework_helper = HomeworkHelper(user_id, role)
    timestamp = homework_helper.timestamp_now
    success = homework_helper.grade_homework(submission_uuid, score)
    # update
    if success:
        UpdateHelper(user_id, role, timestamp=timestamp).submission_graded(submission_uuid, score)
    res_data = dict(
        success=success,
        timestamp=timestamp
    )
    return Response(data=res_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def close(request):
    user_id = request.user.username
    req_data = json.loads(request.body)
    role = req_data['role']
    homework_uuid = req_data['homework_uuid']
    homework_helper = HomeworkHelper(user_id, role)
    success = homework_helper.close_homework(homework_uuid)
    res_data = dict(
        success=success,
        timestamp=homework_helper.timestamp_now
    )
    return Response(data=res_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def get_homework_list(request):
    user_id = request.user.username
    role = request.GET['role']
    classroom_uuid = request.GET['classroom_uuid']
    row_list = HomeworkHelper(user_id, role).get_homework_list_by_classroom(classroom_uuid)
    res_data = dict(
        error=0,
        homeworks=row_list
    )
    return Response(data=res_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def get_submission_list(request):
    user_id = request.user.username
    role = request.GET['role']
    homework_uuid = request.GET['homework_uuid']
    row_list = HomeworkHelper(user_id, role).get_submission_list_by_homework(homework_uuid)
    res_data = dict(
        error=0,
        submissions=row_list
    )
    return Response(data=res_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def get_submission_info(request):
    user_id = request.user.username
    role = request.GET['role']
    submission_uuid = request.GET['submission_uuid']
    info = HomeworkHelper(user_id, role).get_submission_info(submission_uuid)
    comments = CommentHelper(user_id, role).get_list(submission_uuid)
    res_data = dict(
        error=0,
        submission=info,
        comments=comments
    )
    return Response(data=res_data, status=status.HTTP_200_OK)