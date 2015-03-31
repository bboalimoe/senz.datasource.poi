from django.conf.urls import patterns, include, url


urlpatterns = patterns("senz.views.place.LocationRecoView",

    url(r'^usr_loc_tag/$', 'GetUserLocationTags'),
    url(r'^add_near_tag/$', 'AddTraceNearTags'),

                        )