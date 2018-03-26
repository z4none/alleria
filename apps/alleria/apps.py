from django.apps import AppConfig


class AlleriaConfig(AppConfig):
    name = 'apps.alleria'

    # 分页大小
    page_size = 15

    # 默认用户密码
    default_password = "88888888"
