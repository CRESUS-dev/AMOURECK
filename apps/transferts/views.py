from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .services import TransfertService
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    UpdateView,
    CreateView,
)
from .models import *
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .forms import *


class PhoneOperatorListView(LoginRequiredMixin, ListView):
    model = PhoneOperator
    template_name = "transferts/phoneOperators_list.html"
    context_object_name = "operators"
    ordering = ["-updated_at"]


class PhoneOperatorCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = PhoneOperator
    form_class = PhoneOperatorAddForm
    template_name = "transferts/phone0perator_add.html"
    success_url = reverse_lazy("operators_list")
    success_message = "Opérateur téléphonique créé avec succès"


class PhoneOperatorEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = PhoneOperator
    form_class = PhoneOperatorAddForm
    template_name = "transferts/phone0perator_add.html"
    success_url = reverse_lazy("operators_list")
    success_message = "Opérateur téléphonique modifié avec succès"


class PhoneOperatorDeleteView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    DeleteView,
):
    model = PhoneOperator
    success_url = reverse_lazy("operators_list")
    success_message = "Opérateur téléphonique supprimé avec succès"


class SimCardListView(LoginRequiredMixin, ListView):
    model = SimCard
    template_name = "transferts/simCard_list.html"
    context_object_name = "simcards"
    ordering = ["-updated_at"]


class SimCardCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = SimCard
    template_name = "transferts/simCard_add.html"
    form_class = SimCardAddForm
    success_url = reverse_lazy("simcards_list")
    success_message = "La carte SIM est ajoutée avec succès"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class SimCardEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = SimCard
    template_name = "transferts/simCard_add.html"
    form_class = SimCardAddForm
    success_url = reverse_lazy("simcards_list")
    success_message = "La carte SIM est modifiée avec succès"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class SimCardDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = SimCard
    success_url = reverse_lazy("simcards_list")
    success_message = "La carte SIM est supprimée avec succès"


class TransferListView(LoginRequiredMixin, ListView):
    model = Transfert
    template_name = "transferts/transfert_list.html"
    context_object_name = "transferts"
    ordering = ["-updated_at"]


class TransfertAddView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Transfert
    form_class = TransfertAddForm
    template_name = "transferts/transfert_add.html"
    success_url = reverse_lazy("transfert_list")
    success_message = "Le transfert est effectué avec succès"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        cleaned = form.cleaned_data

        sim_card = cleaned["sim_card"]
        amount = cleaned["amount"]
        commission = cleaned["commission_amount"]
        operation_type = cleaned["operation_type"]

        # sim_currency = sim.currency_id
        # On récupère l'agence de la session
        agency_id = self.request.session.get("agency_id")

        if not agency_id:
            form.add_error(None, "Aucune agence trouvée dans la session.")
            return self.form_invalid(form)

        exclude = {"sim_card", "amount", "commission_amount", "operation_type"}
        extra_kwargs = {k: v for k, v in cleaned.items() if k not in exclude}

        # Appel du service avec agency obligatoire
        try:
            self.object = TransfertService.create_transfert(
                sim_card=sim_card,
                amount=amount,
                commission_amount=commission,
                operation_type=operation_type,
                agency_id=agency_id,
                currency_id=sim_card.currency,
                **extra_kwargs,
            )
        except Exception as e:
            form.add_error(None, f"Erreur service : {e}")
            return self.form_invalid(form)

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):

        return super().form_invalid(form)


def simcard_context(request):
    sim_id = request.GET.get("sim_id")

    try:
        sim = SimCard.objects.get(id=sim_id)
        return JsonResponse(
            {
                "currency": (
                    sim.currency.code if hasattr(sim.currency, "code") else sim.currency
                ),
                "balance": str(sim.balance),
            }
        )
    except SimCard.DoesNotExist:
        return JsonResponse({"error": "SIM non autorisée"}, status=403)
