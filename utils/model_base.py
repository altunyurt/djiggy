# ~*~ coding:utf-8 ~*~

from django.db import models
from django.db.models.query import QuerySet
from django.forms.models import model_to_dict

import logging
logger = logging.getLogger(__name__)

class QuerySetManager(models.Manager):
    def get_query_set(self):
        """
            Eger bir class icinde queryset tanimi yapilmamissa ilk yuklemede patliyor.
            Asagidaki kontrol bunu engelliyor
        """
        if hasattr(self.model, 'QuerySet'):
            return self.model.QuerySet(self.model)

        elif self.model._meta.fields:
            return QuerySet(self.model)

    def __getattr__(self, attr, *args):

        ''' ozel methodlari aramaya kalktindiga maximum recursion problemi doguyor '''
        if attr.startswith("_"): # or at least "__"
            raise AttributeError
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)

    def first(self, *args, **kwargs):
        qs = self.get_query_set().filter(*args, **kwargs)
        return qs and qs[0] or None

class _Model(models.Model):
    """
        UNCached abstract Model class for enabling simple addition of chainable
        manager methods to models.
    """
    objects = QuerySetManager()

    class Meta:
        abstract = True

    def to_dict(self):
        d = model_to_dict(self, fields=[field.name for field in self._meta.fields])
        d.update(model_to_dict(self, fields=[field.name for field in self._meta.many_to_many]))
        return d

    def update(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.save()
        return self

