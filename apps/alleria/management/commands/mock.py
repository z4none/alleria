from django.core.management.base import BaseCommand
from apps.alleria.models import Menu, User, Role, Permission, PermissionGroup
from faker import Faker
from django.utils.timezone import utc, localtime

import random


class Command(BaseCommand):
    help = "mock data"

    def handle(self, *args, **options):
        Menu.objects.all().delete()

        Menu.objects.create(
            key="system",
            name=u"系统管理",
            url="",
            icon="fa-cog",
            level=1
        ).save()

        Menu.objects.create(
            key="user",
            name=u"用户管理",
            url="/a/user_list",
            icon="fa-user",
            level=2
        ).save()

        Menu.objects.create(
            key="menu",
            name=u"菜单管理",
            url="/a/menu_list",
            icon="fa-bars",
            level=2
        ).save()

        Menu.objects.create(
            key="role",
            name=u"角色管理",
            url="/a/role_list",
            icon="fa-star",
            level=2
        ).save()

        print("-" * 40)

        User.objects.all().delete()
        fake = Faker("zh_CN")
        user_list = []
        for i in range(1000):
            name = fake.name()
            user = User(
                name=fake.name(),
                username=fake.user_name() + fake.user_name(),
                email=fake.free_email(),
                last_login=localtime(fake.past_datetime(tzinfo=utc)),
                last_login_ip=fake.ipv4()
            )
            user_list.append(user)
            print("user {}".format(name))
        User.objects.bulk_create(user_list)

        print("-" * 40)

        groups = []
        PermissionGroup.objects.all().delete()
        for i in range(10):
            group = PermissionGroup(
                name=u"权限组{}".format(i)
            )
            group.save()
            groups.append(group)
            print("permission group {}".format(i))

        print("-" * 40)

        Permission.objects.all().delete()
        for i in range(10):
            for j in range(random.randint(0, 20)):
                permission = Permission(
                    name=u"权限{},{}".format(i, j),
                    code="{},{}".format(i, j),
                    group=groups[i],
                    description="description"
                )
                permission.save()
                print("permission {},{}".format(i, j))

        print("-" * 40)

        Role.objects.all().delete()
        roles = []
        for i in range(10):
            role = Role(
                name=u"角色{}".format(i),
                description=u"角色{}描述".format(i)
            )
            roles.append(role)
            print("role {}".format(i))
        Role.objects.bulk_create(roles)
