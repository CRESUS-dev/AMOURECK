from django.urls import path, include
from .views import *

urlpatterns = [
    path('ticket/Add/', TicketCreateView.as_view(), name='ticket_add'),
    path('ticket/list/', TicketListView.as_view(), name='ticket_list'),
    path('ticket/edit/<int:pk>/', TicketEditView.as_view(), name='ticket_edit'),
    path('ticket/delete/<int:pk>/', TicketDeleteView.as_view(), name='ticket_delete'),
    path('ticket/detail/<int:pk>/', TicketDetailView.as_view(), name='ticket_detail'),
    path('ticket/print/<int:pk>/', ticket_render_pdf_view, name='ticket_print'),
]
