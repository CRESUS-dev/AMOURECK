from .models import *
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TicketForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string
from .models import Ticket


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'passengers/ticket_add.html'
    success_url = reverse_lazy('ticket_list')

    def get_context_data(self, **kwargs):
        customer_id =0
        # retrieve the existant context
        context = super().get_context_data(**kwargs)
        # ✅ add customers for the bootstrap model
        context['customers'] = Customer.objects.all().order_by('lastName')

        # --- PRESERVE selected customer when the form is re-rendered (POST with errors) ---
        selected =None

        if self.request.method == "POST":
            customer_id = self.request.POST.get('customer_id')
        else:
            customer_id = self.request.GET.get('customer_id')

        if customer_id:
            try:
                selected = Customer.objects.get(pk=customer_id)
            except Customer.DoesNotExist:
                selected = None

        context['selected_customer'] = selected

        return context


    # get the selected country currency
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


    def form_valid(self, form):
        agency_id = self.request.session.get('agency_id')
        customer_id = self.request.POST.get('customer_id')

        form.instance.agency_id = agency_id

        # associer le client sélectionné
        if customer_id:
            from apps.customer.models import Customer
            form.instance.customer_id = customer_id
        return super().form_valid(form)


class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'passengers/tickets_list.html'
    context_object_name = "tickets"
    paginate_by = 10
    ordering = ['agency']

class TicketEditView(LoginRequiredMixin, UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'passengers/ticket_add.html'
    success_url = reverse_lazy('ticket_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customers'] = Customer.objects.all().order_by('lastName')

        # Récupère le client du ticket en édition
        ticket = self.object
        context['selected_customer'] = getattr(ticket, 'customer', None)
        return context

class TicketDeleteView(LoginRequiredMixin, DeleteView):
    model = Ticket
    success_url = reverse_lazy('ticket_list')


