from rest_framework import serializers
from .models import *


class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['userid', 'username', 'aliasname', 'email', 'mobile', 'position', 'head_images', 'joined_time',
                  'last_login_time', 'last_login_ip', 'is_admin', 'is_active', 'last_set_pwd_time', 'last_set_pwd_ip']


class DepartmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class UserTokenSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserToken
        fields = '__all__'


class MailTokenSerializers(serializers.ModelSerializer):
    class Meta:
        model = MailToken
        fields = '__all__'


class UserDepartRelationSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserDepartRelation
        fields = '__all__'
