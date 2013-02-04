# -*- coding: utf-8 -*-

import os.path as op
PROJECT_ROOT = op.abspath(op.dirname(op.dirname(__file__)))

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 25

JINJA_EXTENSIONS = ['djtemps.jinja_extensions.Markdown2Extension', 'jinja2.ext.with_', 'jinja2.ext.i18n']
JINJA_METHODS = ['djtemps.jinja_methods.url_for','djtemps.jinja_methods.logger']

