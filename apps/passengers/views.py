from .models import *
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TicketForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'passengers/ticket_add.html'
    success_url = ('tickets_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ✅ Ajouter tous les clients ici pour le modal
        context['customers'] = Customer.objects.all().order_by('lastName')
        return context