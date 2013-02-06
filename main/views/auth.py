# ~*~ coding: utf-8 ~*~

from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from djtemps import render_to_response
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from main.forms import LoginForm, RegisterForm


def wikiLogout(request):
    logout(request)
    return HttpResponseRedirect("/")


def wikiLogin(request):
    registerForm = RegisterForm()
    if request.method == "POST":
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            cdata = loginForm.cleaned_data
            user = authenticate(email=cdata.get("email"), 
                                password=cdata.get("password"))
            if user:
                login(request, user)
                return HttpResponseRedirect("/")
            messages.error(request, _("Wrong email or password "))

    else:
        loginForm = LoginForm()
    return render_to_response("auth/login_or_register.jinja", locals())


def wikiRegister(request):
    if request.method == "POST":
        registerForm = RegisterForm(request.POST)
        if registerForm.is_valid():
            cdata = registerForm.cleaned_data
            user = User.objects.create(email=cdata.get("email"),
                                      username=cdata.get("email"))
            user.set_password(cdata.get("password"))
            user.save()
            return HttpResponseRedirect("/")
    else:
        registerForm = RegisterForm()
    return render_to_response("auth/login_or_register.jinja", locals())
