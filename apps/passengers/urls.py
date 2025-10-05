from django.urls import path, include
from .views import *

urlpatterns = [
    path('ticket/Add/', TicketCreateView.as_view(), name='ticket_add'),

]
