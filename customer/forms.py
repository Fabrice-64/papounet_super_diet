"""
    This module is a personalization of the forms proposed by Django.
    They are to be used for account creation and authentication.

    Classes:
        LoginForm

        UserRegistrationForm

    Exceptions:
        NIL

    Functions:
        NIL
"""
import re
from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from django.contrib.auth.models import User
from .functions import check_password
import re


class LoginForm(forms.Form):
    username = forms.CharField(label="Pseudo")
    password = forms.CharField(label="Mot de Passe",
                               widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Mot de Passe",
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmation du Mot de Passe",
                                widget=forms.PasswordInput)
    email = forms.EmailField(label="Courriel", required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
        labels = {'username': "Pseudo ",
                  'first_name': "Prénom "
                  }
        help_texts = {
            'username': "Max. 150 car. (chiffres\
                , lettres ou les signes + - _ @)"}
        
    def clean_password2(self):
        cd = self.cleaned_data
        check_password(cd['password'], cd['password2'])
        return cd['password2']


class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(label='Mot de Passe Actuel', widget=forms.PasswordInput)
    new_password = forms.CharField(label="Nouveau Mot de Passe", widget=forms.PasswordInput, initial="")
    new_password2 = forms.CharField(label="Confirmation", widget=forms.PasswordInput, initial="")

    def clean_new_password2(self):
        cd = self.cleaned_data
        if cd['current_password'] == cd['new_password2']:
            raise forms.ValidationError(
                "L'ancien et le nouveau mot de passe doivent être différents")
        check_password(cd['new_password'], cd['new_password2'])
        return cd['new_password2']

