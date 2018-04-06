from django.core.management.base import BaseCommand
from apps.alleria.models import Menu, User, Role, Permission, PermissionGroup, DictionaryType, DictionaryItem
from faker import Faker
from django.utils.timezone import utc, localtime

import random


class Command(BaseCommand):
    help = "mock data"

    def handle(self, *args, **options):
        Menu.objects.all().delete()

        Menu.objects.create(
            code="system",
            name=u"系统管理",
            url="",
            icon="fa-cog",
            level=1,
            enabled=True
        ).save()

        Menu.objects.create(
            code="user",
            name=u"用户管理",
            url="/a/user_list",
            icon="fa-user",
            level=2,
            enabled=True
        ).save()

        Menu.objects.create(
            code="menu",
            name=u"菜单管理",
            url="/a/menu_list",
            icon="fa-bars",
            level=2,
            enabled=True
        ).save()

        Menu.objects.create(
            code="role",
            name=u"角色管理",
            url="/a/role_list",
            icon="fa-star",
            level=2,
            enabled=True
        ).save()

        Menu.objects.create(
            code="dict",
            name=u"字典管理",
            url="/a/dictionary",
            icon="fa-bookmark",
            level=2,
            enabled=True
        ).save()

        Menu.objects.create(
            code="dept",
            name=u" 部门管理",
            url="/a/department",
            icon="fa-group",
            level=2,
            enabled=True
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

        print("-" * 40)

        DictionaryType.objects.all().delete()
        dictionary_types = []
        for i in range(10):
            dtype = DictionaryType(
                code="type%d" % i,
                name="类型%s" %i
            )
            dictionary_types.append(dtype)
            print("dtype {}".format(i))
        DictionaryType.objects.bulk_create(dictionary_types)

