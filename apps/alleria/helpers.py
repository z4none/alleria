# coding: utf-8

import traceback

from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect, resolve_url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.forms.models import model_to_dict
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode


from .models import User, Menu, Config


class AuthBackend:
    """custom user authentication backend for django"""

    def authenticate(self, username=None, password=None):
        """
        authenticate user with custom user model

        Args:
            username(string): username of the user
            password(string): password of the user

        Returns:
            User: authenticated user instance, None otherwise
        """
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        """get user by user id, None otherwise"""
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None


class LoginRequiredMixin1(object):
    @classmethod
    def as_view(cls, **k):
        view = super(LoginRequiredMixin, cls).as_view(**k)
        return login_required(view)


def sa_required(f):
    def func(request, *a, **k):
        if request.user and request.user.is_sa:
            return f(request, *a, **k)
        return redirect_error(u"需要超级管理员权限", resolve_url("dashboard:index"))
    return func


class SARequiredMixin(object):
    @classmethod
    def as_view(cls, **k):
        view = super(SARequiredMixin, cls).as_view(**k)
        return sa_required(view)





