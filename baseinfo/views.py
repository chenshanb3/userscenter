import json

from django.shortcuts import render

from rest_framework import viewsets
from utils.cryp import *
from .models import *
from .serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
import hashlib
import datetime
from utils.cryp import *
from utils.custom_log import log_start
from utils.ldap_mad import *

'''
def authentication(request):
    ret = {'code': 404, 'msg': "", 'token': ''}
    if request.method == 'POST':
        ruserid = request.POST.get("userid")
        rpassword = request.POST.get("password")
        try:
            luser = UserProfile.objects.get(userid=ruserid)
            if luser.userid == ruserid and decrypt_p(luser.password) == rpassword:
                ntoken = md5(luser.userid)
                UserToken.objects.create(userid=luser.userid, token=ntoken)
                ret['token'] = ntoken
                ret['code'] = 200
                ret['msg'] = "登录成功"
            else:
                ret['code'] = 403
                ret['msg'] = "用户名或密码错误"
        except UserProfile.DoesNotExist:
            ret['code'] = 404
            ret['msg'] = "用户不存在"
    else:
        ret['code'] = 500
        ret['msg'] = "请求不允许"
    return JsonResponse(ret)
'''

RES = {'code': 20000, 'data': '', 'message': 'success'}


class Authentication(APIView):

    def post(self, request):
        # print(request.META['CONTENT_TYPE'])
        ldap_mad_tools = LdapMadTools()
        ruserid = request.data.get("username", None)
        rpassword = request.data.get("password", None)
        if not ruserid or not rpassword:
            return HttpResponse(1)
        rip = request.META['REMOTE_ADDR']
        try:
            luser = UserProfile.objects.get(userid=ruserid)
            if luser.userid == ruserid and decrypt_p(luser.password) == rpassword:
                ntoken = md5(luser.userid)
                try:
                    usertoekn = UserToken.objects.get(userid=luser.userid)
                    usertoekn.token = ntoken
                    usertoekn.save()
                    luser.last_login_ip = rip
                    luser.save()
                except UserToken.DoesNotExist:
                    usertoekn = UserToken.objects.create(userid=luser.userid, token=ntoken)
                serializer = UserTokenSerializers(usertoekn)
                RES['data'] = serializer.data
                return Response(RES)
            else:
                if ldap_mad_tools.ldap_get_vaild(uid=ruserid, password=rpassword):
                    luser.password = encrypt_p(rpassword)
                    luser.save()
        except UserProfile.DoesNotExist:
            if ldap_mad_tools.ldap_get_vaild(uid=ruserid, password=rpassword):
                user_info = ldap_mad_tools.ldap_get_user(ruserid)
                if user_info['userAccountControl'] in [512, 544]:
                    user = UserProfile()
                    user.userid = ruserid
                    user.password = encrypt_p(rpassword)
                    user.joined_time = user_info.get('whenCreated', datetime.datetime.now()).strftime(
                        '%Y-%m-%d %H:%M:%S')
                    user.last_set_pwd_time = user_info.get('pwdLastSet', datetime.datetime.now()).strftime(
                        '%Y-%m-%d %H:%M:%S')
                    user.aliasname = user_info.get('displayName', None)
                    user.first_name = user_info.get('sn', None)
                    user.last_name = user_info.get('givenName', None)
                    user.position = user_info.get('physicalDeliveryOfficeName', None)
                    user.mobile = user_info.get('telephoneNumber', None)
                    user.last_login_ip = rip
                    user.last_login_time = user_info.get('lastLogon', datetime.datetime.now()).strftime(
                        '%Y-%m-%d %H:%M:%S')
                    user.email = user_info.get('mail', None)
                    user.username = user_info.get('sAMAccountName', None)
                    user.save()
                    ntoken = md5(ruserid)
                    usertoekn = UserToken.objects.create(userid=user.userid, token=ntoken)
                    serializer = UserTokenSerializers(usertoekn)
                    RES['data'] = serializer.data
                    return Response(RES)
                elif user_info['userAccountControl'] in [514, 546, 66050]:
                    return Response("域账号被禁用，请联系域管理员")
                elif user_info['userAccountControl'] in [66048]:
                    return Response("域账号可用，但是密码未设置，建议先通过邮箱找回密码")
                else:
                    return Response("域账号状态异常，请联系域管理员")
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserProfileAPIView(APIView):

    def get_obj(self, uid: str) -> UserProfile:
        try:
            return UserProfile.objects.get(userid=uid)
        except UserProfile.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, uid: str = None) -> Response:
        user = self.get_obj(uid)
        serializer = UserProfileSerializers(user)
        return Response(serializer.data)

    def put(self, request, uid: str = None) -> Response:
        user = self.get_obj(uid)
        serializer = UserProfileSerializers(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uid: str = None):
        user = self.get_obj(uid)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserProfileAllAPIView(APIView):

    def get(self, request) -> Response:
        users = UserProfile.objects.all()
        serializer = UserProfileSerializers(users, many=True)
        return Response(serializer.data)

    def post(self, request) -> Response:
        serializer = UserProfileSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentAllAPIView(APIView):

    def get(self, request) -> Response:
        departments = Department.objects.all()
        serializer = DepartmentSerializers(departments, many=True)
        return Response(serializer.data)

    def post(self, request) -> Response:
        serializer = DepartmentSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentAPIView(APIView):

    def get_obj(self, did: int) -> UserProfile:
        try:
            return Department.objects.get(id=did)
        except Department.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, did: int = None) -> Response:
        department = self.get_obj(did)
        serializer = DepartmentSerializers(department)
        return Response(serializer.data)

    def put(self, request, did: int = None) -> Response:
        department = self.get_obj(did)
        serializer = DepartmentSerializers(department, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, did: int = None):
        department = self.get_obj(did)
        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
