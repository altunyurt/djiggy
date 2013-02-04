# ~*~ coding: utf-8 ~*~

from django import forms
from main.models import Page

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        exclude = ("active_revision", "title")


