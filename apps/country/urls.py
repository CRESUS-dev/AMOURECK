from django.urls import path, include
from .views import *

urlpatterns = [
    path('country/Add/', CountryCreateView.as_view(), name='country_add'),
    path('countries/', CountryListView.as_view(), name='countries_list'),
    path('country/edit/<int:pk>/', CountryEditView.as_view(), name='country_edit'),
    path('country/delete/<int:pk>/', CountryDeleteView.as_view(), name='country_delete'),
    path('town/Add/', TownCreateView.as_view(), name='town_add'),
    path('towns/', TownListView.as_view(), name='towns_list'),
    path('town/edit/<int:pk>/', TownEditView.as_view(), name='town_edit'),
    path('town/delete/<int:pk>/', TownDeleteView.as_view(), name='town_delete'),
    path('agency/Add/', AgencyCreateView.as_view(), name='agency_add'),
    path('agencies/', AgencyListView.as_view(), name='agencies_list'),
    path('agency/edit/<int:pk>/', AgencyEditView.as_view(), name='agency_edit'),
    path('agency/delete/<int:pk>/', AgencyDeleteView.as_view(), name='agency_delete'),


]
