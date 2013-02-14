# ~*~ encoding: utf-8 ~*~

from djtemps import render_to_response 

def about_user(request, user_id, full_name):
    return render_to_response("account/about_user.jinja", locals())


def account_settings(request):
    return render_to_response("account/settings.jinja", locals())

