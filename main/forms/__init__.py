# ~*~ coding: utf-8 ~*~

from django import forms
from django.utils.translation import ugettext_lazy as _

class PageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea())
    message = forms.CharField(widget=forms.Textarea(), required=False)


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    password_confirm = forms.CharField(widget=forms.PasswordInput(), required=True)

    def clean_password_confirm(self):
        d = self.cleaned_data
        if d.get("password") != d.get("password_confirm"):
            raise forms.ValidationError(_("Emails don't match"))
