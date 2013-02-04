# ~*~ coding:utf-8 ~*~
import os.path as op
from logging.handlers import SysLogHandler

PROJECT_ROOT = op.dirname(op.dirname(op.abspath(__file__)))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(name)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'verbose'
        },

        'syslog':{
            'level':'DEBUG',
            'class': 'logging.handlers.SysLogHandler',
            'formatter': 'verbose',
            'facility': SysLogHandler.LOG_LOCAL2,
            'address': '/dev/log'
        },
    },
    'loggers': {
        'django': {
            'handlers':['null'],
            'propagate': True,
            'level':'INFO',
        },
        'django.db.backends': {
            'level': 'INFO',
            'handlers': ['syslog'],
        },
        'main' :{
            'handlers': ['syslog'],
            'level': 'INFO',
            'propagate': True,
        },
        'templates' :{
            'handlers': ['syslog'],
            'level': 'INFO',
            'propagate': True,
        },
        'utils' :{
            'handlers': ['syslog'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

