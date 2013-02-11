# ~*~ coding:utf-8 ~*~

from main.models import *
from django.contrib import admin


class RevisionInline(admin.TabularInline):
    model = Revision


class PageAdmin(admin.ModelAdmin):
    inlines = [RevisionInline,]


admin.site.register(Page)
admin.site.register(Revision)
admin.site.register(ActionLog)
