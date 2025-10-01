from django import forms
from .models import Country


# formulaire de création des clients

class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['name','is_active']


        widgets = {
            'name':forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder':'Entrer le nom du pays'
            }),
            'is_active': forms.RadioSelect(attrs={
                'class': 'form-control',

            }),
        }



