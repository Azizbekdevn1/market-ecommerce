from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import JsonResponse, FileResponse
from django.urls import path, reverse
from django.utils.safestring import mark_safe

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

    # addition_list_display = 'image_download',
    #
    # def get_urls(self):
    #     urls = [
    #         path('download-image/<int:pk>', self.download_image_view, name='download-page')
    #     ]
    #     old_urls = super().get_urls()
    #     return urls + old_urls
    #
    def download_image_view(self, request, pk):
        user: User = User.objects.filter(pk=pk).first()
        if user:
            return FileResponse(user.avatar, as_attachment=True)

        return JsonResponse({})

    def get_list_display(self, request):
        return super().get_list_display(request) + self.addition_list_display

    @admin.action(description='Yuklash')
    def image_download(self, obj: UserProxy):
        html = f'<a href="download-image/{obj.pk}" target="_blank"><button>Rasm</button></a>'
        return mark_safe(html)


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
