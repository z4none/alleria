# coding: utf-8

from ..utils import *
from ..helpers import *
from ..models import User, Role
from ..forms import UserCreateForm, UserUpdateForm


class UserList(AListView):
    active_menu = "system.user"
    model = User
    ordering = "-id"
    paginate_by = get_app_config().page_size


class UserDetail(ADetailView):
    active_menu = "system.user"
    model = User


class UserCreate(ACreateView):
    active_menu = "system.user"
    model = User
    form_class = UserCreateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.set_password(form.cleaned_data['raw_password'])
        self.object.save()

        self.success_message = u"{} 创建成功".format(self.object)
        return super().form_valid(form)


class UserUpdate(AUpdateView):
    active_menu = "system.user"
    model = User
    form_class = UserUpdateForm

    def form_valid(self, form):
        password = form.cleaned_data.get('raw_password')
        self.object = form.save(commit=False)

        if password:
            self.object.set_password(password)

        self.object.save()

        self.success_message = u"修改用户信息成功"
        return super().form_valid(form)


class UserDelete(ADeleteView):
    active_menu = "system.user"
    model = User
    template_name_suffix = "_delete"
    success_url = reverse_lazy('user_list')
    success_message = u"删除用户成功"

    def get_object(self, queryset=None):
        """
        可以进行一些判断，比如用户不能删除自己等。。
        Args:
            queryset:

        Returns:

        """
        self.object = super(UserDelete, self).get_object()
        if self.object.id == self.request.user.id:
            raise Http404
        return self.object


class UserResetPassword(AConfirmView):
    active_menu = "system.user"
    model = User
    cancel_url = "user_detail"
    success_url = "user_detail"
    success_message = "重置用户密码成功"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(id=kwargs["pk"])
        context["message"] = "确定重置 {} 的密码吗?".format(user)
        return context

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs["pk"])
        return super(UserResetPassword, self).post(request, *args, **kwargs)


class UserSelectRoles(ATemplateView):
    active_menu = "system.user"
    template_name = "alleria/user_select_roles.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = user = User.objects.get(id=kwargs["pk"])
        context["roles"] = Role.objects.all()
        context["selected_roles"] = user.roles.all()
        return context

    def post(self, request, **kwargs):
        role_selected = request.POST.getlist("role_selected[]")
        roles = Role.objects.filter(id__in=role_selected)
        user = User.objects.get(id=kwargs["pk"])
        user.roles.clear()
        user.roles.add(*roles)

        messages.add_message(request, messages.SUCCESS, '修改用户角色成功')
        return HttpResponseRedirect(reverse("user_detail",  kwargs=kwargs))
