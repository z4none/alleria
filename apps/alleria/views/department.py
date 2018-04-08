# coding: utf-8

from ..utils import *
from ..models import Department


class DepartmentView(ATemplateView):
    active_menu = "system.dept"
    template_name = "alleria/department.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DepartmentList(AJSONView):
    def get(self, request):
        return {
            "items": list(Department.objects.order_by("left").values())
        }


class DepartmentCreate(AJSONView):
    def post(self, request):
        pid = request.POST.get("pid")
        name = request.POST.get("name")

        parent = None

        try:
            if pid:
                parent = Department.objects.get(id=pid)
                Department.objects.filter(right__gte=parent.right).update(right=F("right") + 2)
                Department.objects.filter(left__gte=parent.right).update(left=F("left") + 2)
                department = Department(
                    name=name,
                    parent=parent,
                    left=parent.right,
                    right=parent.right+1
                )
                department.save()
            else:
                prev = Department.objects.latest("right")
                department = Department(
                    name=name,
                    parent=None,
                    left=prev.right+1,
                    right=prev.right + 2
                )
                department.save()
        finally:
            pass

        return {
            "id": department.id,
            "success": True
        }


class DepartmentUpdate(AJSONView):
    def post(self, request):
        id = request.POST.get("id")
        name = request.POST.get("name")
        department = Department.objects.get(id=id)
        if department:
            department.name = name
            department.save()
            return {
                "success": True
            }
        return {
            "success": False
        }


class DepartmentDelete(AJSONView):
    def post(self, request):
        id = request.POST.get("id")
        department = Department.objects.get(id=id)
        if department:
            offset = department.right - department.left + 1
            Department.objects.filter(Q(left__gte=department.left) & Q(right__lte=department.right)).delete()
            Department.objects.filter(right__gte=department.right).update(right=F('right')-offset)
            Department.objects.filter(left__gte=department.right).update(left=F('left') - offset)
        return {
            "success": True
        }


class DepartmentMove(AJSONView):
    def post(self, request):
        id = request.POST.get("id")
        target_id = request.POST.get("target_id")
        move = request.POST.get("move")

        try:
            # lock

            department = Department.objects.get(id=id)

            moving_list = list(Department.objects.filter(Q(left__gte=department.left) & Q(right__lte=department.right)).values_list("id", flat=True))

            width = department.right - department.left + 1
            Department.objects.exclude(id__in=moving_list).filter(right__gte=department.right).update(right=F('right') - width)
            Department.objects.exclude(id__in=moving_list).filter(left__gte=department.right).update(left=F('left') - width)

            target = Department.objects.get(id=target_id)

            if move == "inner":
                pos = target.right
                department.parent = target
            elif move == "prev":
                pos = target.left
                department.parent = target.parent
            elif move == "next":
                pos = target.right + 1
                department.parent = target.parent
            department.save()

            Department.objects.exclude(id__in=moving_list).filter(right__gte=pos).update(right=F('right') + width)
            Department.objects.exclude(id__in=moving_list).filter(left__gte=pos).update(left=F('left') + width)

            offset = pos - department.left
            Department.objects.filter(id__in=moving_list).update(left=F('left') + offset)
            Department.objects.filter(id__in=moving_list).update(right=F('right') + offset)
        finally:
            # unlock
            pass

        return {
            "success": True
        }
