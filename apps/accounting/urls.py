from django.urls import path, include
from .views import *

urlpatterns = [
    path('accounting/Add/', AccountingCreateView.as_view(), name='accounting_add'),
    path('accounting/list', AccountingListView.as_view(), name='accounting_list'),
    path('accounting/edit/<int:pk>/', AccountingListView.as_view(), name='accounting_edit'),



]
