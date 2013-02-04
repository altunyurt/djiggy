# ~*~ coding:utf-8 ~*~
    
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin

urlpatterns = patterns(
    'main.views',
    url(r'^wikiShowSimilarPages/(?P<page_title>\w+)/$', 'wikiShowSimilarPages', name='wikiShowSimilarPages'),
    url(r'^wikiPreviewPage/$', 'wikiPreviewPage', name='wikiPreviewPage'),
    url(r'^wikiCreatePage/(?P<page_title>\w+)/$', 'wikiCreatePage', name='wikiCreatePage'),
    url(r'^wikiEditPage/(?P<page_title>\w+)/$', 'wikiEditPage', name='wikiEditPage'),
    url(r'^(?P<page_title>\w+)$', 'wikiShowPage', name='wikiShowPage'),
    url(r'^$', 'index', name='index'),
)

