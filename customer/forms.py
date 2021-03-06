"""
    This module is a personalization of the forms proposed by Django.
    They are to be used for account creation and authentication.

    Classes:
        LoginForm

        UserRegistrationForm

        PasswordChangeForm

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


class LoginForm(forms.Form):
    username = forms.CharField(label="Pseudo")
    password = forms.CharField(label="Mot de Passe",
                               widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    """
        This class customizes the Django standard form
        dealing with the user registration.
        Main Changes are the labels and the fields.
    """
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
    """
        This class checks the compliance of the new password to some criteria. Very basic in the current
        version: former and new password should be different.
        It calls a function from functions.py which checks whether the password complies with some criteria.
    """
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
