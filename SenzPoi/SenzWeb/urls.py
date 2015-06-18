from django.conf.urls import patterns, include, url
from django.contrib import admin

from senz.urls import urlpatterns as senz_url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SenzWeb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^senz/', include(senz_url))
)
