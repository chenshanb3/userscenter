from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *
from django.urls import *

urlpatterns = [
    path('user-info', UserProfileAllAPIView.as_view()),
    path('user-info/<str:uid>', UserProfileAPIView.as_view()),
    path('department-info', DepartmentAllAPIView.as_view()),
    path('department-info/<int:did>', DepartmentAPIView.as_view()),
    path('auth', Authentication.as_view()),
]
