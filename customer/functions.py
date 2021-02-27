"""
    This module hosts the functions linked to the customization of Django Users.
    functions:
        check_passwords: sets the criteria to authorize a password change.
"""
from django.contrib.auth import forms


def check_password(password1, password2):
    if len(password1) < 8:
        raise forms.ValidationError("Votre mot de passe est trop court")
    if any(map(str.isalpha, password2)) is False:
        raise forms.ValidationError(
            "Votre mot de passe doit comporter au moins une lettre")
    if password1 != password2:
        raise forms.ValidationError(
            "Les mots de passe doivent être identiques")
