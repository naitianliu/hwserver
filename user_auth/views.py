from api.views_set.lib import *
from user_auth.functions.verification_code_helper import VerificationCodeHelper
from user_auth.functions.phone_login_helper import PhoneLoginHelper
from user_auth.functions.profile_helper import ProfileHelper

# Create your views here.


@api_view(['POST'])
def phone_login(request):
    req_data = json.loads(request.body)
    phone_number = req_data['phone']
    password = req_data['password']
    result_tup = PhoneLoginHelper(phone_number).login(password)
    print result_tup
    res_data = dict(
        error=result_tup[0],
        token=result_tup[1]
    )
    return Response(data=res_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def phone_send_verification_code(request):
    req_data = json.loads(request.body)
    phone_number = req_data['phone']
    error_code = VerificationCodeHelper(phone_number).send_code()
    res_data = dict(error=error_code)
    return Response(data=res_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def phone_verify_verification_code(request):
    req_data = json.loads(request.body)
    phone_number = req_data['phone']
    code = req_data['code']
    error_code = VerificationCodeHelper(phone_number).verify_code(code)
    res_data = dict(error=error_code)
    return Response(data=res_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def phone_reset_password(request):
    req_data = json.loads(request.body)
    phone_number = req_data['phone']
    code = req_data['code']
    password = req_data['password']
    result_tup = PhoneLoginHelper(phone_number).reset_password(code, password)
    res_data = dict(
        error=result_tup[0],
        token=result_tup[1]
    )
    return Response(data=res_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def phone_register(request):
    req_data = json.loads(request.body)
    phone_number = req_data['phone']
    code = req_data['code']
    password = req_data['password']
    result_tup = PhoneLoginHelper(phone_number).register(code, password)
    print result_tup
    res_data = dict(
        error=result_tup[0],
        token=result_tup[1]
    )
    return Response(data=res_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def user_profile_update(request):
    username = request.user.username
    req_data = json.loads(request.body)
    nickname = req_data['nickname'] if 'nickname' in req_data else None
    img_url = req_data['img_url'] if 'img_url' in req_data else None
    error_code = ProfileHelper(username).update_profile(nickname=nickname, img_url=img_url)
    res_data = dict(error=error_code)
    return Response(data=res_data, status=status.HTTP_200_OK)