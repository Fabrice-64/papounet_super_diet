"""
    This module deals with all issues directly related to the user or customer.
    The common HTML Code to all apps. is managed from here as well.
    Therefore, if the different apps were to be split, don't forget to transfer
    the relevant code.
    User login, logout and register functions strictly follow\
        Django user's guide.
    Therefore, you can refer to the official documentation !

    Classes:
        NIL

    Exceptions:
        NIL

    Functions:
        user_login

        user_logout

        home:
        simply renders to the home page

        register:
        used to create a new user

        personal_infos:
        just display infos from the user. No input expected.

        terms_of_use
        just display the related piece of information.

        contact
        just display the contact coordinates.

        password_change_done
        reports to the user the successful password change

        password_change
        deals with the password change once logged in.
        Does NOT deal with the case of a forgotten password as the Django views handle it.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user
from .forms import LoginForm, UserRegistrationForm, PasswordChangeForm
from django.http import HttpResponse
from django.contrib import messages
from django.forms import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "customer/home.html")
                else:
                    info = "Votre compte est désactivé"
                    return render(request,
                                  "customer/failed_login.html",
                                  {
                                      'info': info,
                                      'next_step': "create_account"})
            else:
                info = "Vos identifiants sont incorrects"
                return render(request,
                              "customer/failed_login.html",
                              {'info': info, 'next_step': "log_in_again"})
    else:
        form = LoginForm()

    return render(request, "customer/login.html", {'form': form})


def user_logout(request):
    logout(request)
    return render(request, "customer/home.html")


def home(request):
    return render(request, "customer/home.html")


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # Automatic login after registration
            user = authenticate(request,
                                username=user_form.cleaned_data['username'],
                                password=user_form.cleaned_data['password'])
            login(request, user)

            return render(request, 'customer/home.html')
    else:
        user_form = UserRegistrationForm()

    return render(request, "customer/register.html", {'user_form': user_form})


def personal_infos(request):
    return render(request, "customer/personal_infos.html")


def terms_of_use(request):
    return render(request, "customer/terms_of_use.html")


def contact(request):
    return render(request, "customer/contact.html")


def password_change_done(request):
    return render(request, "customer/password_change_done.html")


@login_required
def password_change(request):
    if request.method == "POST":
        user_form = PasswordChangeForm(request.POST)
        if user_form.is_valid():
            user = request.user
            user.set_password(user_form.cleaned_data['new_password'])
            user.save()
            update_session_auth_hash(request, user)
            return render(request, 'customer/password_change_done.html')
    else:
        user_form = PasswordChangeForm()

    return render(request, 'customer/password_change.html', {'form': user_form})
