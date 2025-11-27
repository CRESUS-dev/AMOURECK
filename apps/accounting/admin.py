from django.contrib import admin
from .models import Accounting

@admin.register(Accounting)
class AccountingAdmin(admin.ModelAdmin):
    list_display = ['agency', 'operation_type','date_operation', 'description','amount','commission']
    list_filter = ['agency','operation_type']

