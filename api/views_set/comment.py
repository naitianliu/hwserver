from api.views_set.lib import *
from api.functions.comment_helper import CommentHelper


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