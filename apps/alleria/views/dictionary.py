# coding: utf-8

from ..utils import *
from ..models import DictionaryType, DictionaryItem


class Dictionary(ATemplateView):
    active_menu = "system.dict"
    template_name = "alleria/dictionary.html"

    def get_context_data(self, **kwargs):
        pk = kwargs.get("pk")

        context = super().get_context_data(**kwargs)
        context["types"] = DictionaryType.objects.all().order_by("code")

        current = pk and DictionaryType.objects.get(id=pk)

        if not current:
            current = DictionaryType.objects.all().order_by("code").first()

        context["current"] = current
        context["items"] = current.items.order_by("order")
        return context


class DictionaryTypeCreate(ACreateView):
    active_menu = "system.dict"
    model = DictionaryType
    fields = ['code', 'name']
    success_message = "创建字典类型成功"

    def get_success_url(self):
        return reverse_lazy('dictionary', kwargs={
            "pk": self.object.id
        })


class DictionaryTypeUpdate(AUpdateView):
    active_menu = "system.dict"
    model = DictionaryType
    fields = ['code', 'name']
    success_message = "编辑字典类型成功"

    def get_success_url(self):
        return reverse_lazy('dictionary', kwargs={
            "pk": self.object.id
        })


class DictionaryTypeDelete(ADeleteView):
    active_menu = "system.dict"
    model = DictionaryType
    template_name_suffix = "_delete"
    success_url = reverse_lazy('dictionary')
    success_message = u"删除字典类型成功"


class DictionaryItemCreate(ACreateView):
    active_menu = "system.dict"
    model = DictionaryItem
    fields = ['code', 'name']
    success_message = "添加字典数据成功"

    def form_valid(self, form):
        dictionary_type = DictionaryType.objects.get(id=self.kwargs['pk'])

        self.object = form.save(commit=False)
        self.object.type = dictionary_type

        print(self.object)
        self.object.save()

        self.success_message = u"{} 创建成功".format(self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dictionary', kwargs={
            "pk": self.object.type.id
        })


class DictionaryItemUpdate(AUpdateView):
    active_menu = "system.dict"
    model = DictionaryItem
    fields = ['code', 'name']
    success_message = "编辑字典数据成功"

    def get_success_url(self):
        return reverse_lazy('dictionary', kwargs={
            "pk": self.object.type.id
        })


class DictionaryItemDelete(ADeleteView):
    active_menu = "system.dict"
    model = DictionaryItem
    template_name_suffix = "_delete"
    success_url = reverse_lazy('dictionary')
    success_message = u"删除字典数据成功"

    def get_success_url(self):
        return reverse_lazy('dictionary', kwargs={
            "pk": self.kwargs["type_pk"]
        })


class DictionaryItemReorder(AJSONView):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode("utf-8"))
        for code, order in data.items():
            print(code, order)
            item = DictionaryItem.objects.get(code=code)
            item.order = order
            item.save()
        return {
            "success": True
        }
