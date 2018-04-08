# coding:utf-8

from django import forms

from .models import User, Role, Department
from .utils import *
from .widgets import ZtreeSelect


class UserCreateForm(forms.ModelForm):
    raw_password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(attrs={'readonly': 'readonly'}, render_value=True),
        label=u"密码", initial=get_app_config().default_password,
        help_text=u"默认密码: %s" % get_app_config().default_password)

    department = forms.ModelChoiceField(
        queryset=Department.objects.order_by("left"),
        widget=ZtreeSelect(attrs={"placeholder": "请选择部门", "data-url": reverse_lazy("department_list")}),
        label=u"部门",
        required=False)

    class Meta:
        model = User
        fields = ["username", "name", "email", "is_active", "is_sa", "raw_password", "roles", "department"]


class UserUpdateForm(forms.ModelForm):
    raw_password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput,
        label=u"密码",
        required=False,
        help_text=u"不填写则不修改密码")

    raw_password_repeat = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput,
        label=u"重复密码",
        required=False)

    department = forms.ModelChoiceField(
        queryset=Department.objects.order_by("left"),
        widget=ZtreeSelect(attrs={"placeholder": "请选择部门", "data-url": reverse_lazy("department_list")}),
        label=u"部门",
        required=False)

    class Meta:
        model = User
        fields = ["username", "name", "email", "is_active", "is_sa", "raw_password", "raw_password_repeat", "roles",
                  "department"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["roles"].widget.attrs["size"] = "1"

    def clean(self):
        cleaned_data = super(UserUpdateForm, self).clean()
        raw_password = cleaned_data.get("raw_password")
        raw_password_repeat = cleaned_data.get("raw_password_repeat")

        if raw_password != raw_password_repeat:
            if 'raw_password' not in self._errors:
                from django.forms.utils import ErrorList
                self._errors['raw_password'] = ErrorList()
            self._errors['raw_password'].append("两次密码不一致")

        return self.cleaned_data
