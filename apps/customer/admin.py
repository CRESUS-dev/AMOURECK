from django.contrib import admin
from .models import *
from simple_history.admin import SimpleHistoryAdmin
from simple_history import register
from .models import HistoricalCustomer


@admin.register(Customer)
class CustomerAdmin(SimpleHistoryAdmin):
    list_display = ('code','firstName', 'lastName', 'sex', 'phone_number', 'email', 'IDCardNumber', 'address', 'country','agency')
    list_filter = ('country',)


# Admin du modèle historique avec filtres utiles
@admin.register(HistoricalCustomer)
class HistoricalCustomerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "sex",
        "firstName",
        "lastName",
        "phone_number",
        "email",
        "IDCardNumber",
        "address",
        "country",
        "history_date",
        "history_user",
        "history_type",
    )
    list_filter = ("history_user", "history_date", "history_type", "country")
    search_fields = ("firstName", "lastName", "email", "phone_number")
