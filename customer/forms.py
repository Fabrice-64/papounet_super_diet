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
from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label="Pseudo")
    password = forms.CharField(label="Mot de Passe",
                               widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Mot de Passe",
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmation du Mot de Passe",
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
        labels = {'username': "Pseudo ",
                  'first_name': "Prénom ",
                  'email': "Courriel",
                  }
        help_texts = {
            'username': "Max. 150 car. (chiffres\
                , lettres ou les signes + - _ @)"}

        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password'] != cd['password2']:
                raise forms.ValidationError(
                    "Les mots de passe doivent être identiques")
            return cd['password2']
