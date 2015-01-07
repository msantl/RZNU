from django.conf.urls import patterns, url

from snippy import views

urlpatterns = patterns('',
    # web interface
    url(r'^$', views.index, name='index'),
    url(r'^error/$', views.error, name='error'),

    url(r'login/$', 'django.contrib.auth.views.login'),
    url(r'logout/$', 'django.contrib.auth.views.logout',
        { 'next_page' : '/'}),

    url(r'^new/user/$', views.new_user, name='new_user'),
    url(r'^new/snippet/$', views.new_snippet, name='new_snippet'),

    url(r'^users/$', views.users, name='users'),
    url(r'^snippets/$', views.snippets, name='snippets'),
    url(r'^users/(?P<user_id>\d+)/$', views.user_detail, name='user_detail'),
    url(r'^snippets/(?P<snippet_id>\d+)/$', views.snippet_detail, name='snippet_detail'),

    url(r'^stats/$', views.stats, name='stats'),

    url(r'^api/$', views.api_detail, name='api details'),

    # rest interface
    url(r'^api/users/$', views.api_users, name='api_users'),
    url(r'^api/snippets/$', views.api_snippets, name='api_snippets'),
    url(r'^api/users/(?P<user_id>\d+)/$', views.api_user_detail, name='api_user_detail'),
    url(r'^api/snippets/(?P<snippet_id>\d+)/$', views.api_snippet_detail, name='api_snippet_detail'),

    url(r'^api/stats/$', views.api_stats, name='api_stats_view'),
)

