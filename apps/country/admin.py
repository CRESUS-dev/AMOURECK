from django.contrib import admin
from .models import Country, Town, Agency
from django.utils.html import format_html


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    fields = ("name", "iso_code", "currency", "is_active")

    # @admin.display(description="Devise")
    # def get_currency(self, obj):
    #     return obj.currency


@admin.register(Town)
class TownAdmin(admin.ModelAdmin):
    fields = ("name", "country")


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "code", "image_tag")

    def image_tag(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit: cover;"/>',
                obj.logo.url,
            )
        return "-"

    image_tag.short_description = "logo"
