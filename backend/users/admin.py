from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser, Supplier, Customer


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser


class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('is_supplier', 'is_customer', 'phone')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('is_supplier', 'is_customer')}),
    )
    list_display = ('username', 'email', 'is_supplier',
                    'is_customer', 'is_staff', 'is_superuser')
    list_filter = ('is_supplier', 'is_customer', 'is_staff',
                   'is_superuser', 'is_active')


admin.site.register(CustomUser, CustomUserAdmin)


class SupplierAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username', 'user__email')


admin.site.register(Supplier, SupplierAdmin)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username', 'user__email')


admin.site.register(Customer, CustomerAdmin)
