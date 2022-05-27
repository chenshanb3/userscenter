from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *
from django.urls import *

urlpatterns = [
    path('login_by_username', Authentication.as_view()),
    path('get_info_by_token', GetInfo.as_view()),
    path('logout', Logout.as_view()),
    path('update_by_token', Update.as_view()),
    path('updatepwd_by_token', UpdatePwd.as_view()),
    path('get_mail_token', GetMailToken.as_view()),
]
