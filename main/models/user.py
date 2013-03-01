# ~*~ coding: utf-8 ~*~
from django.contrib.auth.models import User
from utils.model_base import _Model, models, QuerySet
from django.db.models.signals import post_save

__all__ = ["Profile", "User"]


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

def create_profile(sender, **kwargs):
    if kwargs.get("created"):
        Profile.objects.create(user=kwargs.get("instance"))

post_save.connect(create_profile, sender=User, dispatch_uid="Create profile")
