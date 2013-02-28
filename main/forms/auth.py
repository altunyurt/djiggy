# ~*~ coding: utf-8 ~*~

from django import forms
from django.utils.translation import ugettext_lazy as _

from main.models import Revision
from main.middleware import get_current_user

class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        if kwargs.pop("has_placeholder", False):
            self.fields["email"] = forms.EmailField(required=True, 
                                                    widget=forms.TextInput(attrs={"placeholder": _("Email address")}))
            self.fields["password"] = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": _("Email address")}), 
                                                      required=True)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    password_confirm = forms.CharField(widget=forms.PasswordInput(), required=True)

    def clean_password_confirm(self):
        d = self.cleaned_data
        if d.get("password") != d.get("password_confirm"):
            raise forms.ValidationError(_("Passwords don't match"))
