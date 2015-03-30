from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^pois/$', include('senz.views.poi.urls')),
    url(r'^activities/$', include('senz.views.activity.urls')),
    url(r'^places/$', include('senz.views.place.urls')),
)




