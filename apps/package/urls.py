from django.urls import path, include
from .views import *

urlpatterns = [
    path('package/Add/', PackageCreateView.as_view(), name='package_add'),
     path('package/list/', PackageListView.as_view(), name='package_list'),
    path('package/edit/<int:pk>/', PackageEditView.as_view(), name='package_edit'),
    path('package/detail/<int:pk>/', PackageDetailView.as_view(), name='package_detail'),
    path('package/delete/<int:pk>/', PackageDeleteView.as_view(), name='package_delete'),
    # path('ticket/print/<int:pk>/', ticket_render_pdf_view, name='ticket_print'),

    path('package/dashboard/', package_dashboard, name='package_dashboard'),
    path('package/dashboard/data/', package_dashboard_data, name='package_dashboard_data'),
]
