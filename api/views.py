import re

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_encode_handler
from rest_framework_jwt.serializers import jwt_payload_handler
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter

from api.filter import LimitFilter, ComputerFilterSet
from api.models import User, Computer
from api.paginations import MyPageNumberPagination, MyLimitPagination, MyCoursePagination
from api.serializers import UserModelSerializer, ComputerModelSerializer
from utils.response import APIResponse
from api.authentication import JWTAuthentication



class UserDetailAPIView(APIView):
    # 只能登陆后才可以访问
    permission_classes = [IsAuthenticated]
    # authentication_classes = [JSONWebTokenAuthentication]
    # 自定义
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        return APIResponse(results={"username": request.user.username})


class LoginAPIView(APIView):
    """
     实现多方式登录如账号，手机，邮箱等登录并签发token：
     实现步骤：
     #1. 禁用权限与认证组件
     #2. 获取前端发送的参数
     #3. 通过参数匹配用户
     #4. 签发token并返回token
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        # 账号使用account  密码使用pwd
        # account = request.data.get("account")
        # pwd = request.data.get("pwd")
        user_ser = UserModelSerializer(data=request.data)
        user_ser.is_valid(raise_exception=True)

        return APIResponse(data_message="ok", token=user_ser.token, results=UserModelSerializer(user_ser.obj).data)

    # 面向过程的开发方式，耦合度过高且代码复杂难以维护，不推荐使用
    # def demo_post(self, request, *args, **kwargs):
    #     account = request.data.get("account")
    #     pwd = request.data.get("pwd")
    #
    #     # 判断登陆方式
    #     if re.match(r'.+@.+', account):
    #         user_obj = User.objects.filter(email=account).first()
    #     elif re.match(r'1[3-9][0-9]{9}', account):
    #         user_obj = User.objects.filter(phone=account).first()
    #     else:
    #         user_obj = User.objects.filter(username=account).first()
    #
    #     # 判断是否合法用户
    #     if user_obj and user_obj.check_password(pwd):
    #         payload = jwt_payload_handler(user_obj)  # 生成载荷信息
    #         token = jwt_encode_handler(payload)  # 生成token
    #         return APIResponse(results={"username": user_obj.username}, token=token) # 签发token
    #     return APIResponse(data_message="程序错误")
class ComputerListAPIView(ListAPIView):
    queryset = Computer.objects.all()
    serializer_class = ComputerModelSerializer
    filter_backends = [SearchFilter, OrderingFilter, LimitFilter, DjangoFilterBackend]    # 配置过滤的器类
    search_fields = ["name", "price"]    # 搜索条件
    ordering = ["price"]# 排序条件

    # 指定分页器
    pagination_class = MyPageNumberPagination
    # pagination_class = MyLimitPagination
    # pagination_class = MyCoursePagination
    # django-filter 查询
    # filter_class = ComputerFilterSet
