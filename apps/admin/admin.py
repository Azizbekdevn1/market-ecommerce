from django.contrib import admin
from django.contrib.admin import StackedInline
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from apps.models import Product, Category, ProductImage, User, Order
from apps.models.product import SiteSetting


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    readonly_fields = ['slug']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class ProductImageStackedInline(StackedInline):
    model = ProductImage
    min_num = 1
    extra = 0
    fields = ['image']


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    inlines = [ProductImageStackedInline]
    list_display = ['id', 'name', 'price']


@admin.register(SiteSetting)
class SiteSettingModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, *args, **kwargs):
        return False


# @admin.register(User)
class UserUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'),
         {'fields': (
             'first_name', 'last_name', 'email', 'avatar', 'workout', 'country', 'is_verified', 'banner', 'intro',
             'phone')}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'avatar'),
        }),
    )
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
#
#
# admin.site.unregister(Group)
