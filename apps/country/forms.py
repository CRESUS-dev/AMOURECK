from django import forms
from .models import Country, Town, Agency




class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['name','iso_code','currency','is_active']



        widgets = {
            'name':forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder':'Entrer le nom du pays'
            }),
            'iso_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrer le code ISO'
            }),
            'currency': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrer la devise'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',  # Bootstrap pour checkbox
            }),

        }

class TownForm(forms.ModelForm):
    class Meta:
        model=Town
        fields = ['name', 'country']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrer le nom de la ville',

            }),
            'country': forms.Select(attrs={
                'class': 'form-select select2',
                'placeholder':'Sélectionner un pays'

            }),
        }

class AgencyForm(forms.ModelForm):
    class Meta:
        model=Agency
        fields = ['name', 'country', 'code','address','phone','logo']
        labels = {
            'name':'Nom agence',
            'country':'Pays'
        }

        widgets = {
        'name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Entrer la dénomination de l'agence",

        }),
        'country': forms.Select(attrs={
            'class': 'form-select select2',
            'placeholder':'Sélectionner un pays'

        }),
        'code': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Saisir le code de l'agence"

        }),
        'address': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Saisir l'adresse de l'agence"
        }),
        'phone': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Numéro téléphone"
        }),
        'logo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
    }

