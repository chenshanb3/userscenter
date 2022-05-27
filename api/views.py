from baseinfo.serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime
from utils.cryp import *
from utils.ldap_mad import *
from django.core.mail import send_mail
import requests
from django.utils.decorators import method_decorator
from django.conf import settings

RES = {'code': 20000, 'data': '', 'message': 'success'}


def check_token(func):
    def wrapper(request, *args, **kwargs):
        allow_paths = ['/api/v1/extend/login_by_username', '/api/v1/extend/logout']
        path = request.path_info
        if path in allow_paths:
            return func(request, *args, **kwargs)
        try:
            if request.method == 'GET':
                rtoken = request.GET.get('token')
            else:
                rtoken = request.data.get('token')
            print(rtoken)
            try:
                print(UserToken.objects.get(token=rtoken))
                time_login = UserToken.objects.get(token=rtoken).creat_time
                time_now = datetime.datetime.now()
                if (time_now - time_login).seconds < 1800:
                    return func(request, *args, **kwargs)
                else:
                    UserToken.objects.get(token=rtoken).delete()
                    RES2 = {'code': 50014, 'data': '', 'message': 'token失效，请重新登录'}
                    return Response(RES2)
            except UserToken.DoesNotExist:
                RES2 = {'code': 50014, 'data': '', 'message': 'token无效，请重新登录'}
                return Response(RES2)
        except:
            RES2 = {'code': 50014, 'data': '', 'message': 'token无失效，请重新登录'}
            return Response(RES2)

    return wrapper


class Authentication(APIView):

    def post(self, request):
        ldap_mad_tools = LdapMadTools()
        ruserid = request.data.get("username", None)
        rpassword = request.data.get("password", None)
        if not ruserid or not rpassword:
            RES2 = {'code': 20001, 'data': '', 'message': '账号密码异常'}
            return Response(RES2)
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
                if user_info['userAccountControl'] in [512, 544, 60080]:
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
                    user.mobile = user_info.get('mobile', None)
                    user.last_login_ip = rip
                    user.last_login_time = user_info.get('lastLogon', datetime.datetime.now()).strftime(
                        '%Y-%m-%d %H:%M:%S')
                    user.email = user_info.get('mail', None)
                    user.username = user_info.get('sAMAccountName', None)
                    user.save()
                    ntoken = md5(user.userid)
                    usertoekn = UserToken.objects.update_or_create(userid=user.userid, token=ntoken)
                    serializer = UserTokenSerializers(usertoekn)
                    RES['data'] = serializer.data
                    return Response(RES)
                elif user_info['userAccountControl'] in [514, 546, 66050]:
                    RES2 = {'code': 20001, 'data': '', 'message': '域账号被禁用，请联系域管理员'}
                    return Response(RES2)
                elif user_info['userAccountControl'] in [66048]:
                    RES2 = {'code': 20001, 'data': '', 'message': '域账号可用，但是密码未设置，建议先通过邮箱找回密码'}
                    return Response(RES2)
                else:
                    RES2 = {'code': 20001, 'data': '', 'message': '域账号状态异常，请联系域管理员'}
                    return Response(RES2)
            RES2 = {'code': 20001, 'data': '', 'message': '域账号状态异常，请联系域管理员'}
            return Response(RES2)


class GetInfo(APIView):

    @method_decorator(check_token)
    def get(self, request):
        rtoken = request.GET.get("token", None)
        if rtoken:
            userid = UserToken.objects.get(token=rtoken).userid
            user = UserProfile.objects.get(userid=userid)
            serializer = UserProfileSerializers(user)
            RES['data'] = serializer.data
            return Response(RES)
        return Response(RES)
        # if check_token(request):
        #     rtoken = request.GET.get("token", None)
        #     if rtoken:
        #         userid = UserToken.objects.get(token=rtoken).userid
        #         user = UserProfile.objects.get(userid=userid)
        #         serializer = UserProfileSerializers(user)
        #         RES['data'] = serializer.data
        #         return Response(RES)
        #     return Response(RES)
        # else:
        #     RES2 = {'code': 50014, 'data': '', 'message': 'token失效，请重新登录'}
        #     return Response(RES2)


class Logout(APIView):

    def post(self, request):
        rtoken = request.data.get("token", None)
        if not rtoken:
            return Response(RES)
        UserToken.objects.get(token=rtoken).delete()
        return Response(RES)


class Update(APIView):

    @method_decorator(check_token)
    def put(self, request):
        infoFrom = request.data.get("data", None)
        try:
            user = UserProfile.objects.get(userid=infoFrom['userid'])
            user.username = infoFrom['username']
            user.aliasname = infoFrom['aliasname']
            user.mobile = infoFrom['mobile']
            user.position = infoFrom['position']
            user.save()
            return Response(RES)
        except UserProfile.DoesNotExist:
            RES2 = {'code': 20001, 'data': '', 'message': '域账号更新异常，请联系域管理员'}
            return Response(RES2)


class UpdatePwd(APIView):

    @method_decorator(check_token)
    def post(self, request):
        mailtoken = request.data.get("mailtoken", None)
        emailid = request.data.get("emailid", None)
        password = request.data.get("password", None)
        ip = request.META['REMOTE_ADDR']
        user_email = emailid + '@izkml.com'
        token = MailToken.objects.get(email=user_email)
        if token.token == mailtoken and token.apply_ip == ip:
            lt = LdapMadTools()
            if lt.ldap_update_password(uid=emailid, pwd=password):
                return Response(RES)
            # try:
            #     user = UserProfile.objects.get(userid=emailid)
            #     if user.email == user_email:
            #         user.password = encrypt_p(password)
            #         user.save()
            #         token.delete()
            #         lt = LdapMadTools()
            #         if lt.ldap_update_password(uid=emailid, pwd=password):
            #             return Response(RES)
            #         else:
            #             return Response(RES)
            # except UserProfile.DoesNotExist:
            #     pass
        return Response(RES)


class GetMailToken(APIView):

    def get(self, request):
        emailid = request.GET.get("emailid", None)
        user_email = emailid
        userid = str(emailid).split('@')[0]
        ip = request.META['REMOTE_ADDR']
        token = md5(emailid)
        try:
            lt = MailToken.objects.get(userid=userid)
            lt.apply_ip = ip
            lt.token = token
            lt.save()
        except MailToken.DoesNotExist:
            MailToken.objects.create(email=user_email, userid=emailid, apply_ip=ip, token=token)
        send_mail(
            subject='域账号邮箱验证码',
            message='您的验证码为: {}'.format(token),
            from_email=settings.EMAIL_HOST_USER,  # 发件人邮箱地址
            recipient_list=[user_email],
            fail_silently=False
        )
        return Response(RES)
