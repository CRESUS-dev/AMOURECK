from django import forms
from djmoney.money import Money
from .models import Package


class PackageForm(forms.ModelForm):

    class Meta:
        model = Package

        fields = [
            "departure_town",
            "arrival_town",
            "description",
            "price",
            "receiver_name",
            "receiver_phone",
            "package_count",
            "payment_method",
            "mobile_money_phone_number",
            "status",
        ]
        widgets = {
            "departure_town": forms.Select(
                attrs={
                    "class": "form-select select2",
                    "data-placeholder": "Choisir une ville...",
                }
            ),
            "arrival_town": forms.Select(
                attrs={
                    "class": "form-select select2",
                    "data-placeholder": "Choisir une ville...",
                }
            ),
            "description": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Entrer la description du colis",
                }
            ),
            "receiver_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Entrer le nom et prénoms du receveur",
                }
            ),
            "package_count": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Ex: 2"}
            ),
            "payment_method": forms.Select(
                attrs={
                    "class": "form-select select2",
                    "data-placeholder": "Choisir un moyen de paiement",
                }
            ),
            "mobile_money_phone_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "+224622000000"}
            ),
            "receiver_phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ex: +224622000000"}
            ),
            "status": forms.Select(
                attrs={
                    "class": "form-select select2",
                    "data-placeholder": "Choisir l'état de paiement",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        """Display only the session currency and lock it"""
        self._request = kwargs.get("request")  # stock the request
        request = kwargs.pop(
            "request", None
        )  # remove request before calling parent constructor
        super().__init__(*args, **kwargs)
        # 1) get currency from the sessin

    def clean(self):
        """Ville départ != arrivée."""
        cleaned_data = super().clean()
        dep = cleaned_data.get("departure_town")
        arr = cleaned_data.get("arrival_town")
        if dep and arr and dep == arr:
            self.add_error(
                "arrival_town",
                "La ville de départ doit être différente de la ville d'arrivée.",
            )
        return cleaned_data
