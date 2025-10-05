from django.contrib import admin
from .models import Country, Town, Agency


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    fields = ('name','iso_code','currency', 'is_active')


@admin.register(Town)
class TownAdmin(admin.ModelAdmin):
    fields = ('name','country')


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    fields = ('name', 'country','code')
