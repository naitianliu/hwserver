from django.conf.urls import url
from user_auth.views import *

urlpatterns = [
    url(r'^phone/login/', phone_login),
    url(r'^phone/verification_code/send/', phone_send_verification_code),
    url(r'^phone/verification_code/verify/', phone_verify_verification_code),
    url(r'^phone/reset_password/', phone_reset_password),
    url(r'^phone/register/', phone_register),

    url(r'^user/profile/update/', user_profile_update),

]