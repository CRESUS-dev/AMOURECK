from django.urls import path, include
from .views import *

urlpatterns = [
    path('customer/Add/', CustomerCreateView.as_view(), name='customer_add'),
    path('customers/', CustomerListView.as_view(), name='customers_list'),
    path('customer/edit/<int:pk>/', CustomerUpdateView.as_view(), name='customer_edit'),
    path('customer/delete/<int:pk>/', CustomerDeleteView.as_view(), name='customer_delete'),
]
