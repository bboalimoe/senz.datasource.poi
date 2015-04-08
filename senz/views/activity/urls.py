from django.conf.urls import patterns, include, url

urlpatterns = patterns('senz.views.activity.ActivityMappingView',

    url(r'^initiate_map/$', 'InitiateMapping'),
    url(r'^activity/$', 'GetActivitiesById'),
)
