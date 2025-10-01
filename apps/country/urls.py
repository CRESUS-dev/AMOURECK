from django.urls import path, include
from .views import *

urlpatterns = [
    path('country/Add/', CountryCreateView.as_view(), name='country_add'),
    path('countries/', CountryListView.as_view(), name='countries_list'),
    path('country/edit/<int:pk>/', CountryEditView.as_view(), name='country_edit'),
    path('country/delete/<int:pk>/', CountryDeleteView.as_view(), name='country_delete'),
]
