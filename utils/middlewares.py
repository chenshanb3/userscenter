from django.utils.deprecation import MiddlewareMixin


class HeradsCors(MiddlewareMixin):
    """
    跨域中间件
    """

    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = '*'
        # 如果是简单请求这样即可，但是我们一般方送json格式的数据，还有可能会有其他method,所有还要进一步判断
        if request.method == 'OPTIONS':
            # 复杂请求会先发预检
            response["Access-Control-Allow-Headers"] = "Content-Type"
            response["Access-Control-Allow-Methods"] = "GET,PUT,PATCH,DELETE"
        if request.method == 'GET':
            # 复杂请求会先发预检
            response["Access-Control-Allow-Headers"] = "Content-Type"
            response["Access-Control-Allow-Methods"] = "GET,PUT,PATCH,DELETE"
        return response

# class CheckToken(MiddlewareMixin):
#     def view_test(self, request, response):
#         username = request.POST.get('username')
#         token = request.POST.get('token')
#         tokens = UserToken.objects.filter(user_id=username).first()
#         if token == tokens:
#             return response
#         else:
#             return 'login'
