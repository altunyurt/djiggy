# ~*~ coding: utf-8 ~*~

from utils.model_base import _Model, models, QuerySet
from django.contrib.auth.models import User
import re

# matches single _s only, two or more _s will be left untouched
re_title = re.compile(r"(?<!_)_(?!_)")

class Revision(_Model):
    """ sayfanın eski sürümüne göre diffi 
        sayfa her güncellendiğinde bu kısma bir diff atmak gerekiyor
    """
    page = models.ForeignKey("Page", related_name="revisions")
    content = models.TextField(null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=False)
    message = models.TextField(null=True)

    def __unicode__(self):
        return u"%s %s" % (self.page.title, self.datetime)


class Page(_Model):
    PAGE_STATUS = (
        ("1", "Active"),
        ("2", "Locked"),
        ("3", "Suspended"),
        ("4", "Needs Review")
    )
    title = models.CharField(max_length=255, blank=False, unique=True, null=False)
    revision = models.ForeignKey(Revision, related_name="_", null=True)
    status = models.CharField(max_length=1, choices=PAGE_STATUS, default="1")

    def __unicode__(self):
        return u"%s" % self.title.replace("_", " ")

    class QuerySet(QuerySet):
        def get_similar_pages(self, page_title):
            return self.filter()

    def patch(self, patch_list):
        return True

    def as_dict(self):
        return {"content": self.revision.content, "title": self.title}

    @property
    def readable_title(self):
        """ any single _s will be replaced with space character. if there's more than one _s,
        then those will be replaced with single _ character"""
        return re_title.sub(" ", self.title).replace("__", "_")

    @property
    def locked(self):
        return self.status == "2"

    @property
    def needs_review(self):
        return self.status == "4"

    @property
    def suspended(self):
        return self.status == "3"

