from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.admin import UserUserAdmin
from apps.models import User
from apps.proxies import OperatorProxy, AdminProxy, CurrierProxy, UserProxy, ManageerProxy


@admin.register(AdminProxy)
class AdminProxyModelAdmin(UserAdmin):
    list_display = ['username']

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type=User.Type.ADMIN)


@admin.register(CurrierProxy)
class CurrierProxyModelAdmin(UserAdmin):
    list_display = ['username']

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type=User.Type.CURRIER)


@admin.register(UserProxy)
class UserProxyModelAdmin(UserUserAdmin):
    pass


@admin.register(OperatorProxy)
class OperatorProxyModelAdmin(UserAdmin):
    list_display = ['username']

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type=User.Type.OPERATOR)


@admin.register(ManageerProxy)
class ManageerProxyModelAdmin(UserAdmin):
    list_display = ['username']

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type=User.Type.MANAGER)
