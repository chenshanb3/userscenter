from django.utils.deprecation import MiddlewareMixin
from baseinfo.models import UserToken
from django.http import JsonResponse
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import HttpResponse
from django.http.response import HttpResponseBase
from django.http import Http404

RES2 = {'code': 50014, 'data': '', 'message': 'token失效，请重新登录'}


# class TokenExpired(HttpResponseBase):
#     status_code = 200


class CheckToken(MiddlewareMixin):
    pass
    # def process_request(self, request):
    #     allow_paths = ['/api/v1/extend/login_by_username', '/api/v1/extend/logout']
    #     path = request.path_info
    #     if path in allow_paths:
    #         return None
        # else:
        #     try:
        #         if request.method == 'GET':
        #             rtoken = request.GET.get('token')
        #         else:
        #             rtoken = request.data.get('token')
        #         print(rtoken)
        #         try:
        #             time_login = UserToken.objects.get(token=rtoken).creat_time
        #             time_now = datetime.now()
        #             if (time_now - time_login).seconds < 1800:
        #                 return None
        #             else:
        #                 UserToken.objects.get(token=rtoken).delete()
        #                 raise Http404
        #         except UserToken.DoesNotExist:
        #             raise Http404
        #     except:
        #         raise Http404

    # def process_request(self, request):
    #     allow_paths = ['/login', '/auth', '/api/v1/user-info']
    #     path = request.path_info
    #     for allow_path in allow_paths:
    #         if path == allow_path:
    #             return None
    # return HttpResponse(404)

    # ip = request.META['REMOTE_ADDR']
    # print(request.META)
    # print(path, ip)

    # def process_response(self, request, response):
    #     print("middle_first--process_response", time.time())
    #     print(response, type(response))
    #     return response

    # def process_response(self, request, response):
    #     print("开始检查token")
    #     ret = {}
    #     try:
    #         rtoken = request.POST.get('token')
    #         time_login = UserToken.objects.get(token=rtoken).creat_time
    #         time_now = datetime.now()
    #         if (time_now - time_login).seconds < 1800:
    #             return response
    #         else:
    #             UserToken.objects.get(token=rtoken).delete()
    #             return Response(status=status.HTTP_400_BAD_REQUEST)
    #     except:
    #         return Response(1)
