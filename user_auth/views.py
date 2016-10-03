from api.views_set.lib import *
from user_auth.functions.verification_code_helper import VerificationCodeHelper
from user_auth.functions.phone_login_helper import PhoneLoginHelper
from user_auth.functions.profile_helper import ProfileHelper
from user_auth.functions.vendor_login import VendorLogin
from user_auth.functions.invitation_helper import InvitationHelper
from user_auth.functions.bind_account_helper import BindAccountHelper
from user_auth.functions.device_token_helper import DeviceTokenHelper

# Create your views here.


@api_view(['POST'])
def phone_login(request):
    req_data = json.loads(request.body)
    phone_number = req_data['phone']
    password = req_data['password']
    result_tup = PhoneLoginHelper(phone_number).login(password)
    res_data = dict(
        error=result_tup[0],
        token=result_tup[1]
    )
    username = result_tup[2]
    profile = ProfileHelper(username).get_profile()
    if profile:
        res_data['profile'] = profile
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


@api_view(['POST'])
def wechat_login(request):
    req_data = json.loads(request.body)
    uid = req_data['uid']
    nickname = req_data['nickname']
    img_url = req_data['img_url']
    username, token, active = VendorLogin().wechat_login(uid, nickname, img_url)
    res_data = dict(
        error=0,
        username=username,
        token=token,
        active=active
    )
    return Response(data=res_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def generate_invitation_code(request):
    code = InvitationHelper().generate_invitation_code()
    res_data = dict(
        error=0,
        code=code
    )
    return Response(data=res_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def validate_invitation_code(request):
    req_data = json.loads(request.body)
    code = req_data['code']
    uid = req_data['uid'] if 'uid' in req_data else None
    username = req_data['username'] if 'username' in req_data else None
    vendor = req_data['vendor'] if 'vendor' in req_data else None
    result = InvitationHelper().validate_invitation_code(str(code).strip())
    if result and vendor == 'wechat':
        BindAccountHelper().activate_account(username, "wechat", uid)
    res_data = dict(
        error=0,
        valid=result
    )
    return Response(data=res_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def update_device_token(request):
    username = request.user.username
    req_data = json.loads(request.body)
    device_token = req_data['device_token']
    DeviceTokenHelper(username).add_update_device_token(device_token)
    res_data = dict(
        error=0
    )
    return Response(data=res_data, status=status.HTTP_200_OK)