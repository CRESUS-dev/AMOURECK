from django.urls import path, include
from .views import *

urlpatterns = [
    path('customerAdd/', CustomerCreateView.as_view(), name='customer_add'),
    path('customers_list/', CustomerListView.as_view(), name='customers_list')
]
