from django.shortcuts import render
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import  AccountingForm
from django.views.generic import ListView,DetailView,DeleteView,CreateView,UpdateView
from django.contrib.messages.views import  SuccessMessageMixin
class AccountingCreateView(LoginRequiredMixin, CreateView):
    model = Accounting
    form_class = AccountingForm
    success_url = reverse_lazy('accounting_list')
    template_name = "accounting/accounting_add.html"
    success_message ="Opération enregistrée avec succès"

    def form_valid(self, form):
        agency_id = self.request.session.get('agency_id')
        form.instance.agency_id = agency_id

        return super().form_valid(form)

class AccountingListView(LoginRequiredMixin, ListView):
    model = Accounting
    template_name = "accounting/accounting_list.html"
    context_object_name = "accounting"
    paginate_by = 10
    ordering = ['-updated_at']

    def get_context_data(self, **kwargs):
        """injecter la liste des agences dans le context"""
        context = super().get_context_data(**kwargs)
        agencies = Agency.objects.order_by('name').distinct()
        context['agencies'] = agencies
        return context






