from django.urls import path, include
from .views import *

urlpatterns = [
    path('ticket/Add/', TicketCreateView.as_view(), name='ticket_add'),
    path('ticket/list/', TicketListView.as_view(), name='ticket_list'),
    path('ticket/edit/<int:pk>/', TicketEditView.as_view(), name='ticket_edit'),
    path('ticket/delete/<int:pk>/', TicketDeleteView.as_view(), name='ticket_delete'),
    path('ticket/print/<int:pk>/', ticket_print, name='ticket_print'),
]
