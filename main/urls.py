# ~*~ coding:utf-8 ~*~
    
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to

urlpatterns = patterns(
    'main.views.auth',
    url(r'^auth/login/', 'wiki_login', name='wiki_login'),
    url(r'^auth/register/', 'wiki_register', name='wiki_register'),
    url(r'^auth/logout/', 'wiki_logout',  name='wiki_logout'),
)

urlpatterns += patterns(
    'main.views',
    url(r'^wiki_show_similar_pages/(?P<page_title>\w+)/$', 'wiki_show_similar_pages', name='wiki_show_similar_pages'),
    url(r'^wiki_preview_page/$', 'wiki_preview_page', name='wiki_preview_page'),
    url(r'^wiki_create_page/(?P<page_title>\w+)/$', 'wiki_create_page', name='wiki_create_page'),
    url(r'^wiki_edit_page/(?P<page_title>\w+)/$', 'wiki_edit_page', name='wiki_edit_page'),
    url(r'^wiki_list_revisions/(?P<page_title>\w+)/$', 'wiki_list_revisions', name='wiki_list_revisions'),
    url(r'^wiki_revert_page_to_revision/(?P<page_title>\w+)/(?P<revision_id>\d+)/$', 'wiki_revert_page_to_revision',
        name='wiki_revert_page_to_revision'),
    url(r'^wiki_show_diffs/(?P<page_title>\w+)/(?P<revision1>\w+)/(?P<revision2>\w+)/$', 'wiki_show_diffs', name='wiki_show_diffs'),
    url(r'^wiki_show_user/(?P<user_id>\d+)(?:/(?P<full_name>\w+))?/$', 'wiki_show_user', name='wiki_show_user'),
    url(r'^(?P<page_title>\w+)/$', 'wiki_show_page', name='wiki_show_page'),
    url(r'^$', redirect_to, {"url": "/Index"}),
)

