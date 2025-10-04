from django import forms
from .models import Country, Town




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

class TownForm(forms.ModelForm):
    class Meta:
        model=Town
        fields = ['name', 'country']
        labels = {
            'name':'Nom ville',
            'country':'Pays'
        }

    widgets = {
        'name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrer le nom de la ville',

        }),
        'country': forms.Select(attrs={
            'class': 'form-control',
            'placeholder':'Sélectionner un pays'

        }),
    }

