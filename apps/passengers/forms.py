# forms.py
from django import forms
from djmoney.money import Money
from .models import Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'departure_town',
            'arrival_town',
            'departure_date',
            'departure_hour',
            'ticket_price',
            'payment_method',
            'mobile_money_phone_number',
        ]
        widgets = {
            'departure_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'departure_hour': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'mobile_money_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'departure_town': forms.Select(attrs={'class': 'form-select'}),
            'arrival_town': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        """Display only the session currency and lock it."""
        self._request = kwargs.get('request')
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # 1) devise depuis la session (fallback XOF)
        currency = 'XOF'
        if request and hasattr(request, 'session'):
            currency = request.session.get('currency', 'XOF')

        field = self.fields.get('ticket_price')

        # --- CAS le plus courant : MoneyField -> MultiValueField (amount + currency) ---
        if field and hasattr(field, 'fields') and len(field.fields) > 1:
            # a) restreindre le SOUS-CHAMP devise
            currency_subfield = field.fields[1]
            currency_subfield.choices = [(currency, currency)]

            # b) indiquer la devise par défaut côté form field
            try:
                field.default_currency = currency
            except Exception:
                pass

            # c) renforcer au niveau du widget (select devise)
            try:
                field.widget.widgets[1].choices = [(currency, currency)]
                # rendre visuellement non modifiable (ou remplacer par HiddenInput si tu préfères)
                field.widget.widgets[1].attrs.update({
                    'readonly': True,
                    'style': 'background-color:#f8f9fa;cursor:not-allowed;',
                })
            except Exception:
                pass

            # d) initial si rien n’est fourni
            if not (self.initial.get('ticket_price') or getattr(self.instance, 'ticket_price', None)):
                self.initial['ticket_price'] = Money(0, currency)

        # --- CAS alternatif : champ séparé 'ticket_price_currency' exposé par la form ---
        if 'ticket_price_currency' in self.fields:
            from django.forms import HiddenInput
            self.fields['ticket_price_currency'].choices = [(currency, currency)]
            self.fields['ticket_price_currency'].initial = currency
            self.fields['ticket_price_currency'].widget = HiddenInput()

    def clean_ticket_price(self):
        """Verrouille la devise côté serveur (anti-triche)."""
        money = self.cleaned_data['ticket_price']
        cur = 'XOF'
        if getattr(self, '_request', None) and hasattr(self._request, 'session'):
            cur = self._request.session.get('currency', 'XOF')
        return Money(money.amount, cur)

    def clean(self):
        """Ville départ != arrivée."""
        cleaned_data = super().clean()
        dep = cleaned_data.get('departure_town')
        arr = cleaned_data.get('arrival_town')
        if dep and arr and dep == arr:
            self.add_error('arrival_town', "La ville de départ doit être différente de la ville d'arrivée.")
        return cleaned_data
