from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


# Create your models here.
class UserProfile(models.Model):
    """用户基础信息表"""

    userid = models.CharField(_('用户唯一标识，登录使用'), primary_key=True, max_length=30)  # 用户唯一标识，非ID，登录使用
    password = models.CharField(_('用户密码'), max_length=255, blank=True, null=True)  # 用户密码
    username = models.CharField(_('用户英文名'), max_length=30, blank=True, null=True)  # 用户英文名
    first_name = models.CharField(_('姓'), max_length=30, blank=True, null=True)
    last_name = models.CharField(_('名'), max_length=30, blank=True, null=True)
    aliasname = models.CharField(_('用户中文名'), max_length=30, blank=True, null=True)  # 用户中文名
    email = models.EmailField(_('用户邮箱'), max_length=30, blank=True, null=True)  # 用户邮箱
    mobile = models.CharField(_('用户手机号'), max_length=16, blank=True, null=True)  # 用户手机号，后期也可作为登录使用
    position = models.CharField(_('用户的位置，座位号'), max_length=255, blank=True, null=True)  # 用户的位置，座位号
    head_images = models.URLField(_('用户头像'), max_length=255, blank=True, null=True)  # 用户头像，集成七牛云、阿里云等oss仓库
    joined_time = models.DateTimeField(_('账号创建时间'), blank=True, null=True)  # 账号创建时间
    last_login_time = models.DateTimeField(_('用户最后一次登录的时间'), blank=True, null=True, auto_now=True)  # 用户最后一次登录的时间
    last_login_ip = models.GenericIPAddressField(_('用户最后一次登录的ip'), blank=True, null=True,
                                                 default="0.0.0.0")  # 用户最后一次登录的ip
    is_admin = models.BooleanField(_('是否为管理员'), default=0)  # 是否为管理员
    is_active = models.BooleanField(_('是否禁用'), default=1)  # 是否可用
    last_set_pwd_time = models.DateTimeField(_('密码最后一次设置的时间'), blank=True, null=True)  # 密码最后一次设置的时间
    last_set_pwd_ip = models.GenericIPAddressField(_('密码最后一次设置的ip'), blank=True, null=True,
                                                   default="0.0.0.0")  # 密码最后一次设置的ip


class Department(models.Model):
    """部门基础信息表：公司0级部门"""

    departmentid = models.CharField(_('部门唯一标识'), max_length=30, blank=True, null=True)  # 部门唯一标识，非ID
    department_name = models.CharField(_('部门名称'), max_length=30, blank=True, null=True)  # 部门名称
    department_level = models.IntegerField(_('部门级别（0级部门）'), default=1)  # 部门级别（0级部门）
    department_parent = models.IntegerField(_('父级部门ID'), blank=True, null=True)  # 父级部门ID


class UserDepartRelation(models.Model):
    """员工和部门的关系表"""

    department_id = models.IntegerField(_('部门ID'), )  # 部门ID
    user_id = models.IntegerField(_('用户ID'), )  # 用户ID
    joined_time = models.DateTimeField(_('员工加入部门时间'), auto_now_add=True)  # 员工加入部门时间


class UserToken(models.Model):
    """用户登录token表"""

    userid = models.CharField(_('用户登录账号'), primary_key=True, max_length=30)  # 用户登录账号
    token = models.CharField(_('用户token'), max_length=255)  # 用户token
    creat_time = models.DateTimeField(_('token创建时间'), auto_now_add=True)  # token创建时间


class MailToken(models.Model):
    """邮箱token表，用于找回密码"""

    userid = models.CharField(_('用户登录账号'), primary_key=True, max_length=30)  # 用户登录账号
    email = models.EmailField(_('用户邮箱'), max_length=30)  # 用户邮箱
    token = models.CharField(_('邮箱token'), max_length=255)  # 邮箱token
    apply_ip = models.GenericIPAddressField(_('申请邮箱token的ip'), default="0.0.0.0")
