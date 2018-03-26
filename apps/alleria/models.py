# coding: utf-8

from django.conf import settings
from django.db import models
from django.contrib.auth import models as auth_models
from django.urls import reverse


class PermissionGroup(models.Model):
    name = models.CharField(
        max_length=50,
        blank=False,
        verbose_name=u"名称")


class Permission(models.Model):
    name = models.CharField(
        max_length=50,
        blank=False,
        verbose_name=u"名称")

    code = models.CharField(
        primary_key=True,
        max_length=50,
        blank=False,
        verbose_name=u"编码")

    group = models.ForeignKey(
        PermissionGroup,
        on_delete=models.CASCADE,
        related_name="permissions",
        verbose_name=u"组")


class Role(models.Model):
    name = models.CharField(
        max_length=50,
        blank=False,
        verbose_name=u"名称")

    description = models.CharField(
        max_length=100,
        verbose_name=u"描述")

    enabled = models.BooleanField(
        default=True,
        verbose_name=u"启用")

    permissions = models.ManyToManyField(
        Permission,
        verbose_name=u"权限")

    def get_absolute_url(self):
        return reverse('role_detail', args=(self.id,))


class User(auth_models.AbstractBaseUser):
    name = models.CharField(
        max_length=50,
        blank=False,
        verbose_name=u"姓名")

    username = models.CharField(
        max_length=50,
        blank=False,
        unique=True,
        verbose_name=u"用户名")

    need_modify_password = models.BooleanField(
        blank=False,
        default=True,
        verbose_name=u"需要修改密码")

    email = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=u"电子邮件")

    is_active = models.BooleanField(
        choices=((True, "启用"), (False, "禁用")),
        default=True,
        verbose_name=u"活动")

    is_sa = models.BooleanField(
        choices=((True, "是"), (False, "否")),
        default=False,
        verbose_name=u"超级管理员")

    last_login_ip = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=u"最近登录 IP")

    roles = models.ManyToManyField(
        Role,
        verbose_name=u"角色")

    USERNAME_FIELD = 'username'

    def get_username(self):
        return self.username

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def get_absolute_url(self):
        return reverse('user_detail', args=(self.id,))


class Config(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"名称")
    value = models.CharField(max_length=200, verbose_name=u"值")
    description = models.CharField(max_length=100, verbose_name=u"描述")

    def set_value(self, value):
        self.value = value
        self.save()


class Menu(models.Model):
    key = models.CharField(max_length=50)
    name = models.CharField(max_length=20)
    url = models.CharField(max_length=100, blank=True, null=True)
    icon = models.CharField(max_length=20, blank=True, null=True)
    level = models.IntegerField(default=0)
