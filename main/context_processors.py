# ~*~ encoding: utf-8 ~*~

from main.forms import LoginForm

def loginform(request):
    return {"loginForm": LoginForm()}
