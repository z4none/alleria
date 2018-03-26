from django.shortcuts import render
from django.views.generic import TemplateView

from ..utils import *
from ..helpers import *


def index(request):
    return render(request, "alleria/index.html", {
    })


class Foo(AMixin, TemplateView):
    active_menu = "test.foo"
    template_name = "alleria/index.html"


class Success(TemplateView):
    template_name = "alleria/success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = self.request.GET.get("message")
        context['next'] = self.request.GET.get("next")
        return context


class SuccessTest(View):
    def get(self, request):
        return redirect_success("操作成功", reverse_lazy("user_list"))



