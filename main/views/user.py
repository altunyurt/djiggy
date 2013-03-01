# ~*~ encoding: utf-8 ~*~

from djtemps import render_to_response 
from main.forms import AccountForm, ProfileForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages


__all__ = ["view_profile", "profile_settings", "account_settings"]


def view_profile(request, user_id=None, full_name=None):
    user = (user_id is None or request.user.id == user_id) and request.user \
                                        or get_object_or_404(User, is_superuser=False, pk=user_id)
    return render_to_response("user/view_profile.jinja", locals())


def profile_settings(request):
    if request.method == "POST":
        profileform = ProfileForm(request.POST, instance=request.user.profile)
        if profileform.is_valid():
            profileform.save()
            messages.success(request, _("Profile settings successfully updated"))
            return redirect("profile_settings")
        messages.error(request, _("Please fix these errors and resubmit the form"))
    else:
        profileform = ProfileForm(instance=request.user.profile)
    return render_to_response("user/profile_settings.jinja", locals())


def account_settings(request):
    if request.method == "POST":
        accountform = AccountForm(request.POST, instance=request.user)
        if accountform.is_valid():
            accountform.save()
            messages.success(request, _("Account settings successfully updated"))
            return redirect("account_settings")
        messages.error(request, _("Please fix these errors and resubmit the form"))
    else:
        accountform = AccountForm(instance=request.user)
    return render_to_response("user/account_settings.jinja", locals())

