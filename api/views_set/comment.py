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
    submission_uuid = req_data['submission_uuid']
    info = req_data['info']
    comment_helper = CommentHelper(user_id, role)
    result_tup = comment_helper.create(submission_uuid, info)
    success = result_tup[0]
    comment_uuid = result_tup[1]
    # update
    if success:
        homework_helper = HomeworkHelper()
        homework_uuid = homework_helper.get_homework_uuid_by_submission_uuid(submission_uuid)
        if role == "t":
            receiver_user_id = homework_helper.get_submitter_by_submission_uuid(submission_uuid)
            receiver_role = "s"
        else:
            receiver_user_id = homework_helper.get_creator_by_homework_uuid(homework_uuid)
            receiver_role = "t"
        UpdateHelper(user_id, role).new_comment(author_user_id=user_id,
                                                receiver_user_id=receiver_user_id,
                                                receiver_role=receiver_role,
                                                homework_uuid=homework_uuid,
                                                submission_uuid=submission_uuid,
                                                info=info)
    res_data = dict(
        success=success,
        comment_uuid=comment_uuid,
        timestamp=comment_helper.timestamp_now
    )
    return Response(data=res_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def get_list(request):
    user_id = request.user.username
    role = request.GET['role']
    submission_uuid = request.GET['submission_uuid']
    comments = CommentHelper(user_id, role).get_list(submission_uuid)
    res_data = dict(
        error=0,
        comments=comments
    )
    return Response(data=res_data, status=status.HTTP_200_OK)