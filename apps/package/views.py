from django.shortcuts import render
from .models import *
from apps.customer.models import Customer
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import PackageForm
from django.http import request, HttpResponse,JsonResponse
from django.utils.dateparse import parse_date
from datetime import datetime, time
from django.utils.timezone import make_aware
from django.db.models import Sum, Count
from django.contrib.messages.views import SuccessMessageMixin
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


def package_dashboard_data(request):
    # get dates in request
    date_from = request.GET.get("date_from")
    date_to =request.GET.get("date_to")

    qs = Package.objects.all()

    if date_from:
        d_from = parse_date(date_from) #transforme "2025-10-01" → datetime.date(2025, 10, 1)
        dt_from = make_aware(datetime.combine(d_from, time.min)) #crée un datetime à 00:00:00
        qs = qs.filter(updated_at__gte=dt_from) #rend ce datetime “timezone-aware” (compatible avec les champs DateTimeField)

    if date_to:
        d_to = parse_date(date_from)
        dt_to  = make_aware(datetime.combine(d_to, time.max))
        qs =qs.filter(updated_at__lte=dt_to)

    counts = (
        qs.values("agency__name")
          .annotate(total=Count("id"))
          .order_by("agency__name")
    )

    #Montant par agence + devise de l'agence
    currency_path = "agency__country__currency"
    _amounts = (
        qs.values("agency__name", currency_path)
          .annotate(total_amount=Sum("price"))
          .order_by("agency__name")
    )

    # payload pour le front
    amounts = [
        {
            "agency__name":row["agency_name"],
            "total_amount":str(row["total_amount"]),
            "agency_currency": row[currency_path]

        }
        for row in _amounts
    ]

    return JsonResponse({
        "labels": [c["agency__name"] for c in counts],
        "values": [c["total"] for c in counts],
        "amounts": list(amounts),
    })


def package_dashboard(request):
    return render(request, "package/package_dashboard.html")
