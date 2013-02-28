# ~*~ coding: utf-8 ~*~
from django.contrib.auth.models import User
from utils.model_base import _Model, models, QuerySet

class Profile(_Model):
    user = models.OneToOneField(User)
    about = models.TextField(null=True, blank=True)

    class Meta:
        app_label = "main"

# user extras
@property
def full_name(inst):
    return u"%s %s" % (inst.first_name, inst.last_name)

User.add_to_class("full_name", full_name)

