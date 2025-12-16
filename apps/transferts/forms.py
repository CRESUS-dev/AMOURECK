from django import forms
from .models import *


class PhoneOperatorAddForm(forms.ModelForm):

    class Meta:
        model = PhoneOperator
        fields = ["country", "name"]

        widgets = {
            "country": forms.Select(
                attrs={
                    "class": "form-select select2",
                    "placeholder": "Sélectionner un pays",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Saisir le nom de l'opérateur",
                }
            ),
        }


# class SimCardAddForm(forms.ModelForm):
#
#     class Meta:
#         model = SimCard
#         fields = ["operator", "number", "balance", "currency"]
#         labels = {
#             "operator": "Opérateur Télephonique",
#             "number": "Numéro ",
#             "currency": "Devise",
#         }
#
#         widgets = {
#             "operator": forms.Select(
#                 attrs={
#                     "class": "form-select select2",
#                     "data-placeholder": "Selectionner un opérateur",
#                 }
#             ),
#             "number": forms.TextInput(
#                 attrs={"class": "form-control", "placeholder": "+224622000000"}
#             ),
#             "currency": forms.Select(
#                 attrs={
#                     "class": "form-select select2",
#                     "data-placeholder": "Selectionner une devise",
#                 }
#             ),
#         }
#
#     def __init__(self, *args, **kwargs):
#         self._request = kwargs.get("request")
#         request = kwargs.pop("request", None)
#         super().__init__(*args, **kwargs)
#
#         ## only display operators filtered by country
#         if request and hasattr(request, "session"):
#             country_id = request.session.get("country_id")
#
#             if country_id:
#                 self.fields["operator"].queryset = PhoneOperator.objects.filter(
#                     country_id=country_id
#                 )
#
#         # getting session currency
#         currency = "XOF"
#         if request and hasattr(request, "session"):
#             currency = request.session.get("currency", "XOF")
#
#         balance_field = self.fields.get("balance")
#         #  MoneyField -> MultiValueField (amount + currency)
#         if (
#             balance_field
#             and hasattr(balance_field, "fields")
#             and len(balance_field.fields) > 1
#         ):
#             # restreindre le sous-champ devise
#             currency_subfield = balance_field.fields[1]
#             # currency_subfield.choices = [(currency, currency)]
#             currency_subfield.choices = list(
#                 Currency.objects.values_list("code", "code")
#             )
#         # indicate default currency in form field side
#         try:
#             balance_field.default_currency = currency
#         except Exception:
#             pass
#         # c) renforcer au niveau du widget (select devise)
#         # try:
#         #     balance_field.widget.widgets[1].choices = [(currency, currency)]
#         #     # rendre visuellement non modifiable (ou remplacer par HiddenInput si tu préfères)
#         #     balance_field.widget.widgets[1].attrs.update(
#         #         {
#         #             "readonly": True,
#         #             "style": "background-color:#f8f9fa;cursor:not-allowed;",
#         #         }
#         #     )
#         # except Exception:
#         #     pass
#         # d) initial si rien n’est fourni
#         if not (self.initial.get("balance") or getattr(self.instance, "balance", None)):
#             self.initial["balance"] = Money(0, currency)
#
#         balance_field.widget.widgets[0].attrs.update(
#             {
#                 "class": "form-control",
#                 "placeholder": "Saisir le montant",
#                 "style": "font-size:15px;font-weight:bold;",
#             }
#         )
#         # --- styliser currency ---
#         balance_field.widget.widgets[1].attrs.update(
#             {
#                 "class": "form-select",
#                 "style": "background:#f8f9fa;font-weight:bold;cursor:not-allowed;",
#             }
#         )
#
#     # def clean_balance(self):
#     #     # lock currency server side
#     #     money = self.cleaned_data["balance"]
#     #     cur = "XOF"
#     #     if getattr(self, "_request", None) and hasattr(self._request, "session"):
#     #         cur = self._request.session.get("currency", "XOF")
#     #     return Money(money.amount, cur)


class SimCardAddForm(forms.ModelForm):

    class Meta:
        model = SimCard
        fields = ["operator", "number", "balance", "currency"]
        labels = {
            "operator": "Opérateur Télephonique",
            "number": "Numéro ",
            "currency": "Devise",
        }
        widgets = {
            "operator": forms.Select(
                attrs={
                    "class": "form-select select2",
                    "data-placeholder": "Selectionner un opérateur",
                }
            ),
            "number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "+224622000000"}
            ),
            "currency": forms.Select(
                attrs={
                    "class": "form-select select2",
                    "data-placeholder": "Choisir une devise",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        # only display operators filtered by country
        # if request and hasattr(request, "session"):
        #     country_id = request.session.get("country_id")
        #
        #     if country_id:
        #         self.fields["operator"].queryset = PhoneOperator.objects.filter(
        #             country_id=country_id
        #         )


class TransfertAddForm(forms.ModelForm):

    class Meta:
        model = Transfert
        fields = [
            "sim_card",
            "operation_type",
            "number",
            "amount",
            "commission_amount",
            # "currency",
            "screenshot",
        ]
        labels = {
            "sim_card": "Carte SIM",
            "operation_type": "Type opération ",
            "number": "N° du Client",
            "amount": "Montant",
            "commission_amount": "Commission",
            "currency": "Devise",
            "screenshot": "Capture d'écran",
        }

        widgets = {
            "sim_card": forms.Select(
                attrs={
                    "class": "form-select ",
                    "data-placeholder": "Selectionner une carte SIM",
                }
            ),
            "operation_type": forms.Select(
                attrs={
                    "class": "form-select select2",
                    "data-placeholder": "Selectionner le type de l'opération",
                }
            ),
            "amount": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "data-placeholder": "Selectionner le type de l'opération",
                }
            ),
            "commission_amount": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "+224622000000"}
            ),
            "screenshot": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                    "style": "border: 2px solid #6c757d; padding: 10px; cursor: pointer;",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        self._request = kwargs.get("request")
        request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        if request and request.user.is_authenticated:
            if request.user.is_superuser:
                self.fields["sim_card"].queryset = SimCard.objects.all()
            else:
                self.fields["sim_card"].queryset = request.user.simcards.all()

        # ## only display simcard filtered by country
        # if request and hasattr(request, "session"):
        #     country_id = request.session.get("country_id")
        #
        #     if country_id:
        #         self.fields["sim_card"].queryset = SimCard.objects.filter(
        #             operator__country_id=country_id
        #         )

    #     # getting session currency
    #     currency = "XOF"
    #     if request and hasattr(request, "session"):
    #         currency = request.session.get("currency", "XOF")
    #
    #     amount_field = self.fields.get("amount")
    #     #  traitemnt du champ amount_field
    #     if (
    #         amount_field
    #         and hasattr(amount_field, "fields")
    #         and len(amount_field.fields) > 1
    #     ):
    #         # restreindre le sous-champ devise
    #         currency_subfield = amount_field.fields[1]
    #         currency_subfield.choices = [(currency, currency)]
    #     # indicate default currency in form field side
    #     try:
    #         amount_field.default_currency = currency
    #     except Exception:
    #         pass
    #     # c) renforcer au niveau du widget (select devise)
    #     try:
    #         amount_field.widget.widgets[1].choices = [(currency, currency)]
    #         # rendre visuellement non modifiable (ou remplacer par HiddenInput si tu préfères)
    #         amount_field.widget.widgets[1].attrs.update(
    #             {
    #                 "readonly": True,
    #                 "style": "background-color:#f8f9fa;cursor:not-allowed;",
    #             }
    #         )
    #     except Exception:
    #         pass
    #     # d) initial si rien n’est fourni
    #     if not (self.initial.get("amount") or getattr(self.instance, "amount", None)):
    #         self.initial["amount"] = Money(0, currency)
    #
    #     # traitement du champ commission_amount
    #     commission_amount_field = self.fields.get("commission_amount")
    #
    #     if (
    #         commission_amount_field
    #         and hasattr(commission_amount_field, "fields")
    #         and len(commission_amount_field.fields) > 1
    #     ):
    #         # restreindre le sous-champ devise
    #         currency_subfield = commission_amount_field.fields[1]
    #         currency_subfield.choices = [(currency, currency)]
    #
    #     # indicate default currency in form field side
    #     try:
    #         commission_amount_field.default_currency = currency
    #     except Exception:
    #         pass
    #
    #     # c) renforcer au niveau du widget (select devise)
    #     try:
    #         commission_amount_field.widget.widgets[1].choices = [(currency, currency)]
    #         # rendre visuellement non modifiable (ou remplacer par HiddenInput si tu préfères)
    #         commission_amount_field.widget.widgets[1].attrs.update(
    #             {
    #                 "readonly": True,
    #                 "style": "background-color:#f8f9fa;cursor:not-allowed;",
    #             }
    #         )
    #     except Exception:
    #         pass
    #
    #     try:
    #         commission_amount_field.widget.widgets[1].choices = [(currency, currency)]
    #         # rendre visuellement non modifiable (ou remplacer par HiddenInput si tu préfères)
    #         commission_amount_field.widget.widgets[1].attrs.update(
    #             {
    #                 "readonly": True,
    #                 "style": "background-color:#f8f9fa;cursor:not-allowed;",
    #             }
    #         )
    #     except Exception:
    #         pass
    #
    #         # d) initial si rien n’est fourni
    #     if not (
    #         self.initial.get("amount")
    #         or getattr(self.instance, "commission_amount", None)
    #     ):
    #         self.initial["commission_amount"] = Money(0, currency)
    #
    #     amount_field.widget.widgets[0].attrs.update(
    #         {
    #             "class": "form-control",
    #             "placeholder": "Saisir le montant",
    #             "style": "font-size:15px;font-weight:bold;",
    #         }
    #     )
    #     # --- styliser currency ---
    #     amount_field.widget.widgets[1].attrs.update(
    #         {
    #             "class": "form-select",
    #             "style": "background:#f8f9fa;font-weight:bold;cursor:not-allowed;",
    #         }
    #     )
    #
    #     commission_amount_field.widget.widgets[0].attrs.update(
    #         {
    #             "class": "form-control",
    #             "placeholder": "Saisir le montant",
    #             "style": "font-size:15px;font-weight:bold;",
    #         }
    #     )
    #     # --- styliser currency ---
    #     commission_amount_field.widget.widgets[1].attrs.update(
    #         {
    #             "class": "form-select",
    #             "style": "background:#f8f9fa;font-weight:bold;cursor:not-allowed;",
    #         }
    #     )
    #
    # def clean_amount(self):
    #     # lock currency server side
    #     money = self.cleaned_data["amount"]
    #     cur = "XOF"
    #     if getattr(self, "_request", None) and hasattr(self._request, "session"):
    #         cur = self._request.session.get("currency", "XOF")
    #     return Money(money.amount, cur)
    #
    # def clean_commission_amount(self):
    #     # lock currency server side
    #     money = self.cleaned_data["commission_amount"]
    #     cur = "XOF"
    #     if getattr(self, "_request", None) and hasattr(self._request, "session"):
    #         cur = self._request.session.get("currency", "XOF")
    #     return Money(money.amount, cur)
    #
    # def clean_sim_card(self):
    #     sim = self.cleaned_data["sim_card"]
    #     user = self._request.user
    #     if not user.simcards.filter(id=sim.id).exists():
    #         raise forms.ValidationError(
    #             "Vous n'êtes pas autorisé à utiliser cette carte SIM."
    #         )
    #     return sim
