from django.conf.urls import patterns, include, url
from django.contrib import admin

# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rznu.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # snippy urls are in snippy/urls.py
    url(r'', include('snippy.urls')),
)



