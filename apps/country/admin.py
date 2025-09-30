from django.contrib import admin
from .models import Country, Town, Agency


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    fields = ('name',)


@admin.register(Town)
class TownAdmin(admin.ModelAdmin):
    fields = ('name','country')


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    fields = ('name', 'country')
