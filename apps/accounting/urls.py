from django.urls import path, include
from .views import *

urlpatterns = [
    path('accounting/Add/', AccountingCreateView.as_view(), name='accounting_add'),
    path('accounting/list', AccountingListView.as_view(), name='accounting_list'),
    path('accounting/edit/<int:pk>/', AccountingEditView.as_view(), name='accounting_edit'),
    path('accounting/delete/<int:pk>/', AccountingDeleteView.as_view(), name='accounting_delete'),
    path('accounting/dashboard/data',accounting_table, name='accounting_table'),


]
