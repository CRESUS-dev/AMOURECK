from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from  .models import *
from django.contrib.admin.widgets import FilteredSelectMultiple

from django.contrib.auth import authenticate


class CustomLoginForm(AuthenticationForm):
    agency = forms.ModelChoiceField(
        queryset=Agency.objects.filter(is_active=1),
        empty_label="",
        required=True,
        label="Succursale",
        widget=forms.Select(attrs={
            'class': 'form-control ',


        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom d\'utilisateur'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })
    )

    remember_me = forms.BooleanField(
        required=False,
        label="Se souvenir de moi",
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'agencies', 'countries')

    agencies = forms.ModelMultipleChoiceField(
        queryset=Agency.objects.all(),
        widget=FilteredSelectMultiple("Agences", is_stacked=False),
        required=False,
    )
    countries = forms.ModelMultipleChoiceField(
        queryset=Country.objects.all(),
        widget=FilteredSelectMultiple("Pays", is_stacked=False),
        required=False,
    )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'agencies', 'countries')

    agencies = forms.ModelMultipleChoiceField(
        queryset=Agency.objects.all(),
        widget=FilteredSelectMultiple("Agences", is_stacked=False),
        required=False,
    )
    countries = forms.ModelMultipleChoiceField(
        queryset=Country.objects.all(),
        widget=FilteredSelectMultiple("Pays", is_stacked=False),
        required=False,
    )
