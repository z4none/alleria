import json
from django.http.response import HttpResponse


from ..utils import *
from ..models import Menu


class MenuList(AListView):
    active_menu = "system.menu"
    model = Menu


class MenuUpdate(View):
    def post(self, request):
        data = json.loads(request.POST["data"])
        menus = []
        for item in data:
            menu = Menu(
                code=item["code"],
                enabled=item["enabled"],
                name=item["name"],
                icon=item["icon"],
                level=item["level"],
                url=item["url"]
            )
            menus.append(menu)
        Menu.objects.all().delete()
        Menu.objects.bulk_create(menus)

        messages.success(request, "编辑菜单成功")
        return HttpResponseRedirect("menu_list")
