# ~*~ coding: utf-8 ~*~

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
import re

from utils.model_base import _Model, models, QuerySet
from main.middleware import get_current_user, get_remote_ip

# matches single _s only, two or more _s will be left untouched
re_title = re.compile(r"(?<!_)_(?!_)")

CREATED = "1"
UPDATED_TO_REVISION = "2"
REVERTED_TO_REVISION = "3"
RENAMED = "4"
CHANGED_STATUS = "5"
DELETED = "6"

ACTION_FLAGS = (
    (CREATED , "Created"),
    (UPDATED_TO_REVISION , "Updated "),
    (REVERTED_TO_REVISION, "Reverted  "),
    (RENAMED , "Renamed"),
    (CHANGED_STATUS, "Changed status"),
    (DELETED , "Deleted")
)

ACTIVE = "1"
LOCKED = "2"
SUSPENDED = "3"

PAGE_STATUS = (
    (ACTIVE , "Active"),
    (LOCKED , "Locked"),
    (SUSPENDED, "Suspended"),
)


class _Base(_Model):
    class Meta:
        abstract = True

    def _createActionLog(self, action_flag, **kwargs):
        params = {
            "content_type": ContentType.objects.get_for_model(self),
            "object_id": self.id,
            "user": get_current_user(),
            "action_flag": action_flag,
            "ip": get_remote_ip()
        } 
        params.update(kwargs)
        return ActionLog.objects.create(**params)


class Revision(_Base): 
    page = models.ForeignKey("Page", related_name="revisions")
    content = models.TextField(null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    logs = generic.GenericRelation("ActionLog")
    user = models.ForeignKey(User)

    class Meta:
        ordering = ["-datetime"]

    def __unicode__(self):
        return u"%s %s" % (self.page.title, self.datetime)


class Page(_Base):
    title = models.CharField(max_length=255, blank=False, unique=True, null=False)
    revision = models.ForeignKey(Revision, related_name="_", null=True, blank=True)
    status = models.CharField(max_length=1, choices=PAGE_STATUS, default="1")
    logs = generic.GenericRelation("ActionLog")

    def __unicode__(self):
        return u"%s" % self.title.replace("_", " ")

    class QuerySet(QuerySet):
        def get_similar_pages(self, page_title):
            return self.filter()

    def patch(self, patch_list):
        return True

    @property
    def readable_title(self):
        """ any single _s will be replaced with space character. if there's more than one _s,
        then those will be replaced with single _ character"""
        return re_title.sub(" ", self.title).replace("__", "_")

    @property
    def locked(self):
        return self.status == LOCKED

    @property
    def suspended(self):
        return self.status == SUSPENDED

    @property
    def active(self):
        return self.status == ACTIVE
    
    @property
    def current(self):
        return self.revision

    def rename(self, title, **kwargs):
        self.update(title=title)
        return self._createActionLog(RENAMED, **kwargs)

    def lock(self, **kwargs):
        self.update(status=LOCKED)
        return self._createActionLog(CHANGED_STATUS, **kwargs)

    def suspend(self, **kwargs):
        self.update(status=SUSPENDED)
        return self._createActionLog(CHANGED_STATUS, **kwargs)

    def activate(self, **kwargs):
        self.update(status=ACTIVE)
        return self._createActionLog(CHANGED_STATUS, **kwargs)

    def update_to_revision(self, revision, **kwargs):
        self.update(revision=revision)
        return self._createActionLog(UPDATED_TO_REVISION, **kwargs)

    def revert_to_revision(self, revision, **kwargs):
        self.update(revision=revision)
        return self._createActionLog(REVERTED_TO_REVISION, **kwargs)


class ActionLog(_Model):
    action_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    # affected object 
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey("content_type", "object_id")
    # other object 
    content_type_other = models.ForeignKey(ContentType, blank=True, null=True, related_name="_")
    object_id_other = models.PositiveIntegerField(null=True, blank=True)
    content_object_other = generic.GenericForeignKey("content_type_other", "object_id_other")

    action_flag = models.CharField(max_length=1, choices=ACTION_FLAGS)
    message = models.TextField(blank=True)
    ip = models.GenericIPAddressField(null=True)

    def __unicode__(self):
        ct = self.content_type
        co = self.content_object
        
        oct = self.content_type_other
        oco = self.content_object_other

        t = ct and ("%s %s " % (ct.model, ct.model == "page" and co.readable_title or co.id)) or ""
        ot = oct and ("%s %s " % (oct.model, oct.model == "page" and oco.readable_title or oco.id)) or ""

        return "%s %s %s %s" % (t, self.get_action_flag_display(), ot, self.user.full_name)

# user extras
@property
def full_name(inst):
    return u"%s %s" % (inst.first_name, inst.last_name)

User.add_to_class("full_name", full_name)

