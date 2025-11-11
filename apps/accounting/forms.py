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
        if field and hasattr(field, 'fields') and len(field.fields)>1: # vérifie que le champ field existe et possède 2 sous champs
            # a) resteindre le sous champ devise
            currency_subfield = field.fields[1] # récupérer le sous champ de la devise
            currency_subfield.choices = [(currency, currency)] # limiter le choix à la devise de la session

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
            if not (self.initial.get('ticket_price') or getattr(self.instance, 'ticket_price', None)):
                self.initial['ticket_price'] = Money(0, currency)


    def clean_amount(self):
        """verouille la devise côté serveur"""
        money = self.cleaned_data['amount']
        cur = "XOF"
        if getattr(self, '_request', None) and hasattr(self._request, 'session'):
            cur = self._request.session.get('currency', 'XOF')
        return Money(money.amount, cur)


