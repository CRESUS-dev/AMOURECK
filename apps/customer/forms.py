from django import forms
from .models import Customer
from apps.country.models import Agency


# formulaire de création des clients

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['firstName', 'lastName', 'sex', 'phone_number', 'email', 'IDCardNumber','address']
        exclude = ['country']


        widgets = {
            # 'agency': forms.Select(attrs={
            #     'class': 'form-select'
            # }),
            'sex':forms.Select(attrs={
                'class': 'form-select'
            }),
            'firstName': forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Entrez les prénoms'
                }),
                'lastName': forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Entrez le nom'
                }),
                'phone_number': forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': '+33 612345678'
                }),
                'email': forms.EmailInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'exemple@email.com'
                }),
                'address': forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Adresse complète'
                }),
                'IDCardNumber': forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': "N° Pièce d'identité"
                }),


        }

