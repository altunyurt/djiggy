# -*- coding: utf-8 -*-

from django.conf import global_settings 
import os.path as op
PROJECT_ROOT = op.abspath(op.dirname(op.dirname(__file__)))

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 25

JINJA_EXTENSIONS = ['djtemps.jinja_extensions.Markdown2Extension', 'jinja2.ext.with_', 'jinja2.ext.i18n']
JINJA_METHODS = ['djtemps.jinja_methods.url_for','djtemps.jinja_methods.logger']

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + \
                    ('main.context_processors.login_form',)

AUTHENTICATION_BACKENDS = ( 
    #'social_auth.backends.twitter.TwitterBackend',
    #'social_auth.backends.facebook.FacebookBackend',
    #'social_auth.backends.google.GoogleOAuth2Backend',
    #'social_auth.backends.OpenIDBackend',
    'main.auth_backends.UserEmailBackend',
    'main.auth_backends.VerificationCodeBackend',
    'django.contrib.auth.backends.ModelBackend',
) 

AUTH_PROFILE_MODULE = 'main.Profile'
APPEND_SLASH = True
PRODUCTION = True

INDEX_USES_STATIC_VIEW = True
#You can leave this empty only if INDEX_USES_STATIC_VIEW is True
#/ at the end should be preserved if and only if INDEX_PAGE_NAME is anything other than ""
INDEX_PAGE_URL = "Index/"

# obviously obvious exception 
if INDEX_PAGE_URL == "" and not INDEX_USES_STATIC_VIEW:
    raise Exception("""settings.INDEX_URL_PATTERN should be set to anything other than r"^$" when
                        settins.INDEX_USES_STATIC_VIEW is False""")
