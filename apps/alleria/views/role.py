# coding: utf-8

from ..utils import *
from ..models import Role, Permission, PermissionGroup


class RoleList(AListView):
    active_menu = "system.role"
    model = Role
    ordering = "-id"
    paginate_by = get_app_config().page_size


class RoleCreate(ACreateView):
    active_menu = "system.role"
    model = Role
    fields = ['name', 'description', 'enabled']
    success_url = reverse_lazy('role_list')

    def get_success_message(self, cleaned_data):
        return u"创建角色成功"


class RoleDetail(ADetailView):
    active_menu = "system.role"
    model = Role

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["role_permissions"] = self.object.permissions.all().values_list('code', flat=True)
        context["groups"] = PermissionGroup.objects.all()
        return context


class RoleUpdate(AUpdateView):
    active_menu = "system.role"
    model = Role
    fields = ['name', 'description', 'enabled']


class RoleSelectPermissions(View):
    active_menu = "system.role"

    def post(self, request, pk):
        role = Role.objects.get(id=pk)
        role.permissions.clear()
        role.permissions.add(*request.POST.getlist("permissions"))

        messages.add_message(request, messages.SUCCESS, '修改角色权限成功')
        return redirect(role.get_absolute_url())
