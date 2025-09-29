from django.contrib import admin
from .models import *
from django.utils.html import format_html



@admin.register(Enterprise)
class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Address','Phone', 'Head_office','image_tag' )

    def image_tag(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;"/>', obj.logo.url)
        return "-"
    image_tag.short_description = "logo"




