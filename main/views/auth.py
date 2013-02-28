# ~*~ coding: utf-8 ~*~

from django.contrib.auth.models import User
from django.contrib.auth import login as dj_login, logout as dj_logout, authenticate
from djtemps import render_to_response
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from main.forms import LoginForm, RegisterForm

__all__ = ["logout", "login", "register"]


def logout(request):
    dj_logout(request)
    return HttpResponseRedirect("/")


def login(request):
    register_form = RegisterForm()
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cdata = login_form.cleaned_data
            user = authenticate(email=cdata.get("email"), 
                                password=cdata.get("password"))
            if user:
                dj_login(request, user)
                return HttpResponseRedirect(request.COOKIES.get("next", "/"))
            messages.error(request, _("Wrong email or password "))

    else:
        login_form = LoginForm()
    return render_to_response("auth/login_or_register.jinja", locals())


def register(request):
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            cdata = register_form.cleaned_data
            user = User.objects.create(email=cdata.get("email"),
                                      username=cdata.get("email"))
            user.set_password(cdata.get("password"))
            user.save()
            return HttpResponseRedirect("/")
    else:
        register_form = RegisterForm()
    return render_to_response("auth/login_or_register.jinja", locals())
