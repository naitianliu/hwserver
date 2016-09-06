from api.views_set.lib import *
from api.functions.update_helper import UpdateHelper


@api_view(['GET'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def get_updates(request):
    user_id = request.user.username
    role = request.GET['role']
    updates = UpdateHelper(user_id, role).get_all_updates()
    res_data = dict(
        error=0,
        updates=updates
    )
    return Response(data=res_data, status=status.HTTP_200_OK)