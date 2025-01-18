from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # List viewdagi ko'rinadigan maydonlar
    list_display = ('id', 'phone_number', 'name', 'is_staff', 'is_active', 'created_at')
    list_filter = ('is_staff', 'is_active')

    # Foydalanuvchini tahrirlash formasi maydonlari
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal Information', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )

    # Yangi foydalanuvchini qo'shish formasi maydonlari
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'name', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

    search_fields = ('phone_number', 'name')
    ordering = ('-created_at',)

# Admin panelga CustomUser modelini ro‘yxatdan o‘tkazish
admin.site.register(CustomUser, CustomUserAdmin)
