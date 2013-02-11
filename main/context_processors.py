# ~*~ encoding: utf-8 ~*~

from main.forms import LoginForm

def login_form(request):
    return {"login_form": LoginForm()}
