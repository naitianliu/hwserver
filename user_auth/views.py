from api.views_set.lib import *
from user_auth.functions.verification_code_helper import VerificationCodeHelper

# Create your views here.


@api_view(['POST'])
def phone_login(request):
    pass


@api_view(['POST'])
def phone_send_verification_code(request):
    req_data = json.loads(request.POST)
    phone_number = req_data['phone']
    error_code = VerificationCodeHelper(phone_number).send_code()
    res_data = dict(error=error_code)
    return Response(data=res_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def phone_verify_verification_code(request):
    req_data = json.loads(request.POST)
    phone_number = req_data['phone']
    code = req_data['code']
    error_code = VerificationCodeHelper(phone_number).verify_code(code)
    res_data = dict(error=error_code)
    return Response(data=res_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def phone_set_password(request):
    pass
