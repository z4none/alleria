# coding: utf-8

from django.forms.widgets import Widget


class ZtreeSelect(Widget):
    template_name = 'alleria/widget_ztree_select.html'

    def get_context(self, name, value, attrs):
        context = {}
        context['widget'] = {
            'name': name,
            'value': value,
            'text': self.choices.queryset.get(id=value).name if value else "",
            'attrs': self.build_attrs(self.attrs, attrs),
            'template_name': self.template_name
        }

        context["items"] = list(self.choices.queryset.values())
        return context
