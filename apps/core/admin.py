from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe


@admin.register(Enterprise)
class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ("Name", "Address", "Phone", "Head_office", "image_tag")

    def image_tag(self, obj):
        if obj.logo:
            return mark_safe(
                f'<img src="{obj.logo.url}" width="100" height="100" style="object-fit: cover;"/>'
            )
        return "-"

    image_tag.short_description = "Logo"
