from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
# from .forms import *
from .models import CustomUser
from .forms import *
from .models import LoginHistory
from django.utils.html import format_html


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        'username',
        'email',
        'is_staff',
        'is_admin',
        'is_superuser',
        'image_tag'

    )
    list_filter = (
        'is_staff',
        'is_superuser',
        'is_active',
        'countries'
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email','profil_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Assignments', {'fields': ('countries', 'agencies')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'password1', 'password2', 'is_staff', 'is_active', 'agencies', 'countries'),
        }),
    )

    search_fields = ('username', 'email')
    ordering = ('username',)

    def image_tag(self, obj):
        if obj.profil_picture:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;"/>', obj.profil_picture.url)
        return "-"
    image_tag.short_description = "profil picture"

@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'login_time', 'logout_time', 'ip_address', 'user_agent')
    list_filter = ('user', 'login_time', 'logout_time')
    search_fields = ('user__username', 'ip_address', 'user_agent')
