# ~*~ coding: utf-8 ~*~

from django import forms
from django.utils.translation import ugettext_lazy as _

from main.models import Revision
from django.contrib.contenttypes.models import ContentType
from main.middleware import get_current_user

__all__ = ["PageRevisionForm", "RevertRevisionForm"]

class PageRevisionForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={"placeholder": _("Page content")}))
    message = forms.CharField(widget=forms.Textarea(attrs={"placeholder": _("Edit message")}), 
                              required=False)

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



class RevertRevisionForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(), required=True)

    def save(self, page, revision):
        data = self.cleaned_data
        return page.revert_to_revision(revision, 
                                       message=data.get("message"),
                                        content_type_other=ContentType.objects.get_for_model(Revision),
                                        object_id_other=revision.id
                                      )
