from django.shortcuts import render
from django.db.models import Q
from .models import *
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomerForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect




class CustomerCreateView(LoginRequiredMixin, CreateView):

    model = Customer
    form_class = CustomerForm
    template_name = 'customer/customer_add.html'
    success_url = reverse_lazy('customers_list')

    def form_valid(self, form):
        country_id = self.request.session.get('country_id')
        agency_id = self.request.session.get('agency_id')

        if not country_id:
            messages.error(self.request, "Aucun pays sélectionné en session.")
            return self.form_invalid(form)  # affiche l’erreur sur le même formulaire

        # Associer directement l’ID
        form.instance.country_id = country_id
        form.instance.agency_id = agency_id
        
        return super().form_valid(form)





class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customer/customer_add.html'
    success_url = reverse_lazy('customers_list')

    def form_valid(self, form):
        country_id = self.request.session.get('country_id')
        if not country_id:
            messages.error(self.request, "Aucun pays sélectionné en session.")
            return self.form_invalid(form)  # affiche l’erreur sur le même formulaire

        # Associer directement l’ID
        form.instance.country_id = country_id
        return super().form_valid(form)



class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'customer/customers_list.html'
    context_object_name = "customers"
    paginate_by = 10
    ordering = ['lastName']

    # fonction de recherche sur la liste.
    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(firstName__icontains=q) |
                Q(lastName__icontains=q) |
                Q(phone_number__icontains=q)
            )
        return queryset


class CustomerModalListView(LoginRequiredMixin, TemplateView):
    template_name = "customer/customer_modal_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # On récupère tous les clients triés par lastName
        context['customers'] = Customer.objects.all().order_by('lastName')
        return context

class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    success_url = reverse_lazy('customers_list')

    def post(self, request, *args, **kwargs):

        try:
            response = super().post(request, *args, **kwargs)
            messages.success(request, "Le client a été supprimé avec succès")
            return response
        except ProtectedError:
            messages.error(request,
                           "Impossible de supprimer ce client car il est référencé dans d'autres tables")
            """Redirige vers la liste des clients après une erreur."""
            return HttpResponseRedirect(self.success_url)