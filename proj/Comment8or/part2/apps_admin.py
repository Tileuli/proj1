from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


class Part2Config(AppConfig):
    name = 'part2'


class ChangeAdmin(AdminConfig):
    default_site = 'part2.admin.Comment8orAdminSite'
