# ~*~ coding: utf-8 ~*~

from django import forms
from django.utils.translation import ugettext_lazy as _

from main.models import Revision, ActionLog, ContentType
from main.middleware import get_current_user

class PageRevisionForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea())
    message = forms.CharField(widget=forms.Textarea(), required=False)

    def __init__(self, *args, **kwargs):
        initial = kwargs.get("initial")
        if initial:
            initial.pop("message", "")
            kwargs["initial"] = initial
        super(PageRevisionForm, self).__init__(*args, **kwargs)


    def save(self, page):
        data = self.cleaned_data
        revision = Revision.objects.create(page=page,
                                            user=get_current_user(),
                                            content=data.get("content"),
                                          )
        return page.update_to_revision(revision, 
                                       message=data.get("message"),
                                        content_type_other=ContentType.objects.get_for_model(Revision),
                                        object_id_other=revision.id
                                      )

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


class RevertRevisionForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(), required=True)

    def save(self, page, revision):
        data = self.cleaned_data
        return page.revert_to_revision(revision, 
                                       message=data.get("message"),
                                        content_type_other=ContentType.objects.get_for_model(Revision),
                                        object_id_other=revision.id
                                      )
