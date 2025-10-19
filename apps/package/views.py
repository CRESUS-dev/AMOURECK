from django.shortcuts import render
from .models import *
from apps.customer.models import Customer
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import PackageForm

class PackageCreateView(LoginRequiredMixin, CreateView):
    model = Package
    form_class = PackageForm
    template_name = "package/package_add.html"
    success_url = reverse_lazy('package_list')

    def get_context_data(self, **kwargs):
        customer_id =0
        context = super().get_context_data(**kwargs)
        context['customers'] = Customer.objects.all().order_by('lastName')
        # --- PRESERVE selected customer when the form is re-rendered (POST with errors) ---

        selected = None

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


class PackageListView(LoginRequiredMixin, ListView):
    model = Package
    template_name = 'package/package_list.html'
    context_object_name = "packages"
    paginate_by = 10
    ordering = ['-updated_at']


    def get_context_data(self, **kwargs):
        """injecter la liste des agences dans le context"""
        context = super().get_context_data(**kwargs)
        agencies = Agency.objects.order_by('name').distinct()
        context['agencies'] = agencies
        return context


class PackageEditView(LoginRequiredMixin, UpdateView):
    model = Package
    template_name = 'package/package_add.html'
    form_class = PackageForm
    success_url = reverse_lazy('package_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customers'] = Customer.objects.all().order_by('lastName')

        # Récupère le client du ticket en édition
        package = self.object
        context['selected_customer'] = getattr(package, 'customer', None)
        return context


class PackageDeleteView(LoginRequiredMixin, DeleteView):
    model = Package
    success_url = reverse_lazy('package_list')


class PackageDetailView(LoginRequiredMixin, DetailView):
    model = Package
    context_object_name = "package"
    template_name = "package/package_detail.html"



