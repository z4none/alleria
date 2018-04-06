# coding: utf-8

import json

from django.apps import apps
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.http.response import HttpResponse, HttpResponseRedirect , Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.forms.models import model_to_dict
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, FormView, DeleteView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Max, F, Q

from .models import Menu


class AMixin(object):
    active_menu = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ACTIVE_MENU"] = self.active_menu.split(".") if self.active_menu else False
        return context


class AView(AMixin, View):
    pass


class AJSONView(View):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        return JsonResponse(response)


class AListView(AMixin, ListView):
    pass


class ADetailView(AMixin, DetailView):
    pass


class ATemplateView(AMixin, TemplateView):
    pass


class AFormView(AMixin, SuccessMessageMixin, FormView):
    pass


class ACreateView(AMixin, SuccessMessageMixin, CreateView):
    template_name_suffix = "_create"


class AUpdateView(AMixin, SuccessMessageMixin, UpdateView):
    template_name_suffix = "_update"


class ADeleteView(AMixin, SuccessMessageMixin, DeleteView):
    def delete(self, request, *args, **kwargs):
        success_message = self.get_success_message({})
        if success_message:
            messages.success(self.request, success_message)
        return super(ADeleteView, self).delete(request, *args, **kwargs)

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data


class AConfirmView(AMixin, SuccessMessageMixin, TemplateView):
    """common confirm view"""

    template_name = "alleria/confirm.html"
    no_url_name = None
    message = ""
    cancel_url = ""
    success_url = ""

    def post(self, request, *args, **kwargs):
        print (1111111111)
        success_message = self.get_success_message({})
        if success_message:
            messages.success(self.request, success_message)
        success_url = self.get_success_url(**kwargs)
        return HttpResponseRedirect(success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = self.message
        context['cancel'] = self.get_cancel_url(**kwargs)
        return context

    def get_cancel_url(self, **kwargs):
        return reverse(self.cancel_url, kwargs=kwargs)

    def get_success_url(self, **kwargs):
        return reverse(self.success_url, kwargs=kwargs)


def redirect_success(message="", next=""):
    return redirect('{}?{}'.format(reverse_lazy("success"), urlencode({
        "message": message,
        "next": str(next)
    })))


def redirect_error(message="", next=""):
    return redirect(reverse_lazy("error", kwargs={
        "message": message,
        "next": next
    }))


def get_app_config():
    return apps.get_app_config("alleria")


def get_referer(request, default=None):
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return default
    return referer


def get_menu():
    menu = []
    for item in Menu.objects.filter(enabled=True).order_by("id"):
        item = model_to_dict(item)
        if item["level"] == 1:
            menu.append(item)
        else:
            menu[-1].setdefault("children", [])
            menu[-1]["children"].append(item)
    return menu


def contexts(request):
    return {
        "MENU": get_menu()
    }
