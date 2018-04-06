
from django.urls import path, include

from .views import index, user, role, menu, dictionary, department

urlpatterns = [
    path('', index.index, name='index'),
    path('foo', index.Foo.as_view(), name='foo'),
    path('success', index.Success.as_view(), name='success'),
    path('success_test', index.SuccessTest.as_view(), name='success_test'),

    path('user_list', user.UserList.as_view(), name='user_list'),
    path('user_detail/<int:pk>', user.UserDetail.as_view(), name='user_detail'),
    path('user_create', user.UserCreate.as_view(), name='user_create'),
    path('user_update/<int:pk>', user.UserUpdate.as_view(), name='user_update'),
    path('user_delete/<int:pk>', user.UserDelete.as_view(), name='user_delete'),
    path('user_reset_password/<int:pk>', user.UserResetPassword.as_view(), name='user_reset_password'),
    path('user_select_roles/<int:pk>', user.UserSelectRoles.as_view(), name='user_select_roles'),

    path('role_list', role.RoleList.as_view(), name="role_list"),
    path('role_create', role.RoleCreate.as_view(), name="role_create"),
    path('role_detail/<int:pk>', role.RoleDetail.as_view(), name="role_detail"),
    path('role_update/<int:pk>', role.RoleUpdate.as_view(), name="role_update"),
    path('role_select_permissions/<int:pk>', role.RoleSelectPermissions.as_view(), name="role_select_permissions"),

    path('menu_list', menu.MenuList.as_view(), name='menu_list'),
    path('menu_update', menu.MenuUpdate.as_view(), name='menu_update'),

    path('dictionary', dictionary.Dictionary.as_view(), name='dictionary'),
    path('dictionary/<pk>', dictionary.Dictionary.as_view(), name='dictionary'),
    path('dictionary_type_create', dictionary.DictionaryTypeCreate.as_view(), name='dictionary_type_create'),
    path('dictionary_type_update/<pk>', dictionary.DictionaryTypeUpdate.as_view(), name='dictionary_type_update'),
    path('dictionary_type_delete/<pk>', dictionary.DictionaryTypeDelete.as_view(), name='dictionary_type_delete'),
    path('dictionary/<pk>/item_create', dictionary.DictionaryItemCreate.as_view(), name='dictionary_item_create'),
    path('dictionary/<x>/item_update/<pk>', dictionary.DictionaryItemUpdate.as_view(), name='dictionary_item_update'),
    path('dictionary/<type_pk>/item_delete/<pk>', dictionary.DictionaryItemDelete.as_view(), name='dictionary_item_delete'),
    path('dictionary/<pk>/reorder', dictionary.DictionaryItemReorder.as_view(), name='dictionary_item_reorder'),

    path('department', department.DepartmentView.as_view(), name='department'),
    path('department_list', department.DepartmentList.as_view(), name='department_list'),
    path('department_create', department.DepartmentCreate.as_view(), name='department_create'),
    path('department_update', department.DepartmentUpdate.as_view(), name='department_update'),
    path('department_delete', department.DepartmentDelete.as_view(), name='department_delete'),
    path('department_move', department.DepartmentMove.as_view(), name='department_move'),
]


