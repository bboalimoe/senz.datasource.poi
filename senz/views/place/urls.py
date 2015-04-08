from django.conf.urls import patterns, include, url


urlpatterns = patterns("senz.views.place.LocationRecoView",

    url(r'^user/(?P<user_id>[A-Za-z0-9\-]+)$', 'GetUserLocationTags'),
    url(r'^user/(?P<user_id>[A-Za-z0-9\-]+)/tag$', 'AddTraceNearTags'),
    )