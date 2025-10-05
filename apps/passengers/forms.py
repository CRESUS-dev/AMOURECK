from django import forms
from .models import *
class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'customer',
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
            'ticket_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'mobile_money_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'departure_town': forms.Select(attrs={'class': 'form-select'}),
            'arrival_town': forms.Select(attrs={'class': 'form-select'}),
        }
