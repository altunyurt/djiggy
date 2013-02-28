
# ~*~ coding: utf-8 ~*~

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from main.models import Profile

class AccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["about"]


class PasswordForm(forms.Form):
    current_password = forms.CharField(required=True, widget=forms.PasswordInput())
    new_password = forms.CharField(required=True, widget=forms.PasswordInput())
    new_password_confirm = forms.CharField(required=True, widget=forms.PasswordInput())

    def clean_new_password_confirm(self):
        d = self.cleaned_data
        if d.get("new_password") != d.get("new_password_confirm"):
            raise forms.ValidationError(_("Passwords don't match"))
    
