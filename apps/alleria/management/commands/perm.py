from django.core.management.base import BaseCommand
from apps.alleria.models import Menu, User, Role, Permission, PermissionGroup
from faker import Faker
from django.utils.timezone import utc, localtime

import random


class Command(BaseCommand):
    help = "init permission data"

    def handle(self, *args, **options):
        PermissionGroup.objects.all().delete()
        Permission.objects.all().delete()

        with open("permissions.txt", "r", encoding="utf-8") as file:
            group, group_code, permission = None, "", None
            for line in file.readlines():
                line = line.strip()
                is_group = True
                if line.startswith("-"):
                    is_group = False
                    line = line[1:]
                name, code = line.split(":")
                if is_group:
                    group = PermissionGroup(name=name)
                    group_code = code
                    group.save()
                    print(line)
                else:
                    permission = Permission(
                        name=name,
                        code="{}.{}".format(group_code, code),
                        group=group
                    )
                    permission.save()
                    print(line)
