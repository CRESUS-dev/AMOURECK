from django.shortcuts import render
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import AccountingForm
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    CreateView,
    UpdateView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Sum
from django.utils.dateparse import parse_date
from datetime import datetime, time
from django.utils.timezone import make_aware


class AccountingCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Accounting
    form_class = AccountingForm
    success_url = reverse_lazy("accounting_list")
    template_name = "accounting/accounting_add.html"
    success_message = "Opération enregistrée avec succès"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        agency_id = self.request.session.get("agency_id")
        currency_id = self.request.session.get("currency_id")
        form.instance.currency_id = currency_id
        form.instance.agency_id = agency_id

        return super().form_valid(form)


class AccountingListView(LoginRequiredMixin, ListView):
    model = Accounting
    template_name = "accounting/accounting_list.html"
    context_object_name = "accounting"
    paginate_by = 10
    ordering = ["-updated_at"]

    def get_context_data(self, **kwargs):
        """injecter la liste des agences dans le context"""
        context = super().get_context_data(**kwargs)
        agencies = Agency.objects.order_by("name").distinct()
        context["agencies"] = agencies
        return context


class AccountingDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Accounting
    success_url = reverse_lazy("accounting_list")
    success_message = "L'opération a été supprimée avec succès"


class AccountingEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Accounting
    form_class = AccountingForm
    success_url = reverse_lazy("accounting_list")
    template_name = "accounting/accounting_add.html"
    success_message = "L'opération a été modifiée avec succès"


from django.shortcuts import render
from django.db.models import Sum
from django.utils.dateparse import parse_date
from datetime import datetime, time
from .models import Accounting

from django.db.models import Sum
from django.utils.dateparse import parse_date
from .models import Accounting


def accounting_table(request):
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    agency_id = request.GET.get("agency_id")

    operations = Accounting.objects.all().order_by("date_operation")
    agencies = Agency.objects.all()

    # Filtre agence
    if agency_id:
        operations = operations.filter(agency_id=agency_id)

    # Filtre dates
    if date_from:
        operations = operations.filter(date_operation__gte=parse_date(date_from))

    if date_to:
        operations = operations.filter(date_operation__lte=parse_date(date_to))

    # Totaux tableau
    total_charges = operations.filter(operation_type="CH").aggregate(
        total=Sum("amount")
    )["total"]
    total_produits = operations.filter(operation_type="PD").aggregate(
        total=Sum("amount")
    )["total"]

    # ---- DONNÉES POUR LE GRAPHISTIQUE ----
    chart_data = {}

    for ag in agencies:
        ops_ag = operations.filter(agency=ag)
        total_ch = (
            ops_ag.filter(operation_type="CH").aggregate(total=Sum("amount"))["total"]
            or 0
        )
        total_pd = (
            ops_ag.filter(operation_type="PD").aggregate(total=Sum("amount"))["total"]
            or 0
        )

        chart_data[ag.name] = {
            "charges": float(total_ch),
            "produits": float(total_pd),
        }

    context = {
        "operations": operations,
        "total_charges": total_charges,
        "total_produits": total_produits,
        "date_from": date_from,
        "date_to": date_to,
        "agency_id": agency_id,
        "agencies": agencies,
        "chart_data": chart_data,
    }

    return render(request, "accounting/accounting_dashboard.html", context)
