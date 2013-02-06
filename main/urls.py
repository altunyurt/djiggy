# ~*~ coding:utf-8 ~*~
    
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.views.generic.simple import redirect_to

urlpatterns = patterns(
    'main.views.auth',
    url(r'^auth/login/', 'wikiLogin', name='wikiLogin'),
    url(r'^auth/register/', 'wikiRegister', name='wikiRegister'),
    url(r'^auth/logout/', 'wikiLogout',  name='wikiLogout'),
)

urlpatterns += patterns(
    'main.views',
    url(r'^wikiShowSimilarPages/(?P<page_title>\w+)/$', 'wikiShowSimilarPages', name='wikiShowSimilarPages'),
    url(r'^wikiPreviewPage/$', 'wikiPreviewPage', name='wikiPreviewPage'),
    url(r'^wikiCreatePage/(?P<page_title>\w+)/$', 'wikiCreatePage', name='wikiCreatePage'),
    url(r'^wikiEditPage/(?P<page_title>\w+)/$', 'wikiEditPage', name='wikiEditPage'),
    url(r'^wikiShowRevisions/(?P<page_title>\w+)/$', 'wikiShowRevisions', name='wikiShowRevisions'),
    url(r'^wikiShowDiffs/(?P<page_title>\w+)/(?P<revision1>\w+)/(?P<revision2>\w+)/$', 'wikiShowDiffs', name='wikiShowDiffs'),
    url(r'^(?P<page_title>\w+)$', 'wikiShowPage', name='wikiShowPage'),
    url(r'^$', redirect_to, {"url": "/Index"}),
)

