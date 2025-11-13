from django import forms
from .models import Accounting
from djmoney.money import Money


class AccountingForm(forms.ModelForm):
    class Meta:
        model = Accounting
        fields = ['date_operation','operation_type', 'description', 'amount']

        widgets = {
            'date_operation':forms.DateInput(attrs={
                'type':'date',
                'class':'form-control'
            }),
            'operation_type': forms.Select(attrs={
                'class':'form-select select2' ,
                'data-placeholder':"Choisir le type d'opération"
            }),
            'description': forms.TextInput(attrs={
                'class':'form-control',
                'data-placeholder':"Saisir la description de l'opération"
            })

        }
    def __init__(self, *args, **kwargs):
        """display only the session currency and lock it"""
        self._request = kwargs.get('request')
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # 1) get the currency inn the session
        currency ='XOF'


        if request and hasattr(request, 'session'):
            currency = request.session.get('currency', 'XOF')


        field = self.fields.get('amount')
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
            # c) renforcer coté widget (select devise)
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
            if not (self.initial.get('amount') or getattr(self.instance, 'amount', None)):
                self.initial['amount'] = Money(0, currency)

                # --- CAS alternatif : champ séparé 'ticket_price_currency' exposé par la form ---
            if 'amount_currency' in self.fields:
                from django.forms import HiddenInput
                self.fields['amount_currency'].choices = [(currency, currency)]
                self.fields['amount_currency'].initial = currency
                self.fields['amount_currency'].widget = HiddenInput()




    def clean_amount(self):
        """verouille la devise côté serveur"""
        money = self.cleaned_data['amount']
        cur = "XOF"
        if getattr(self, '_request', None) and hasattr(self._request, 'session'):
            cur = self._request.session.get('currency', 'XOF')
        return Money(money.amount, cur)



