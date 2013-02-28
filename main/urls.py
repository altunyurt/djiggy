# ~*~ coding:utf-8 ~*~
    
from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

urlpatterns = patterns(
    'main.views.auth',
    url(r'^auth/login/', 'login', name='login'),
    url(r'^auth/register/', 'register', name='register'),
    url(r'^auth/logout/', 'logout',  name='logout'),
)

urlpatterns += patterns(
    'main.views.user',
    url(r'^user/account/$', 'account_settings', name='account_settings'),
    url(r'^user/profile/(?:(?P<user_id>\d+)(?:/(?P<full_name>\w+))?/)?$', 'view_profile', name='view_profile'),
    url(r'^user/profile/update/(?P<user_id>\d+)(?:/(?P<full_name>\w+))?/$', 'profile_settings',
        name='profile_settings'),
)

urlpatterns += patterns(
    'main.views',
    url(r'^$', 'index', name='index'),
    url(r'^wiki/show_similar_pages/(?P<page_title>\w+)/$', 'show_similar_pages', name='show_similar_pages'),
    url(r'^wiki/preview_page/$', 'preview_page', name='preview_page'),
    url(r'^wiki/create_page/(?P<page_title>\w+)/$', 'create_page', name='create_page'),
    url(r'^wiki/edit_page/(?P<page_title>\w+)/$', 'edit_page', name='edit_page'),
    url(r'^wiki/list_revisions/(?P<page_title>\w+)/$', 'list_revisions', name='list_revisions'),
    url(r'^wiki/revert_page_to_revision/(?P<page_title>\w+)/(?P<revision_id>\d+)/$', 'revert_page_to_revision',
        name='revert_page_to_revision'),
    url(r'^wiki/show_diff/(?P<page_title>\w+)/$', 'show_diffs', name='show_diffs'),
    url(r"^wiki/search/$", "search", name="search"), 
    url(r'^(?P<page_title>\w+)/$', 'view_page', name='view_page'),
)

