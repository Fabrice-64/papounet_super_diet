"""
"""
from django.contrib.auth import forms

def check_password(password1, password2):
    if len(password1) < 8:
        raise forms.ValidationError("Votre mot de passe est trop court")
    if any(map(str.isalpha, password2)) == False:
        raise forms.ValidationError(
            "Votre mot de passe doit comporter au moins une lettre")
    if password1 != password2:
        raise forms.ValidationError(
            "Les mots de passe doivent être identiques")