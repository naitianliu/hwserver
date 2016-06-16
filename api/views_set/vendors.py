from api.views_set.lib import *
from api.vendors.aliyun import AliyunHelper


@api_view(['GET'])
def get_sts_token(request):
    credentials = AliyunHelper().get_sts_token()
    return Response(data=credentials, status=status.HTTP_200_OK)