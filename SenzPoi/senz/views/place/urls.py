from django.conf.urls import patterns, include, url


urlpatterns = patterns("senz.views.place.LocationRecoView",

    url(r'^$', 'get_user_places'),
    url(r'^user/', 'get_user_places_by_id'),
    url(r'^internal/$', 'internal_get_user_places'),
    #url(r'^user/(?P<user_id>[A-Za-z0-9\-]+)/tag/$', 'AddTraceNearTags'),
    )