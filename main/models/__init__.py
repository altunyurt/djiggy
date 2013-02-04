# ~*~ coding: utf-8 ~*~

from utils.model_base import _Model, models, QuerySet
from django.contrib.auth.models import User

class Revision(_Model):
    """ sayfanın eski sürümüne göre diffi 
        sayfa her güncellendiğinde bu kısma bir diff atmak gerekiyor
    """
    page = models.ForeignKey("Page", related_name="revisions")
    diff = models.TextField(null=False)
    datetime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=False)
    message = models.TextField(null=True)

    def __unicode__(self):
        return u"%s diff %s" % (self.page.title, self.datetime)


class Page(_Model):
    """ sayfanın en son hali """
    title = models.CharField(max_length=255, blank=False, unique=True, null=False)
    content = models.TextField(null=True)
    active_revision = models.ForeignKey(Revision, null=True, related_name="_")

    def __unicode__(self):
        return u"%s" % self.title.replace("_", " ")

    class QuerySet(QuerySet):
        def get_similar_pages(self, page_title):
            return self.filter()



    def patch(self, patch_list):
        return True

    def revert_to(self, target_revision):
        changes_to_apply = []
        if self.active_revision.datetime > target_revision.datetime:
            changes_to_apply = self.revisions.filter(datetime__lte=self.active_revision.datetime, 
                                                     datetime__gt=target_revision.datetime)\
                                            .order_by("id")\
                                            .values("diff")
        else:
            changes_to_apply = self.revisions.filter(datetime__gt=self.active_revision.datetime, 
                                                     datetime__lte=target_revision.datetime)\
                                            .order_by("-id")\
                                            .values("diff")
        self.patch(changes_to_apply)

    def as_dict(self):
        return {"content": self.content, "title": self.title}

