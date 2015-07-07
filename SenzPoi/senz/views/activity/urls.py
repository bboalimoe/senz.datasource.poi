from django.conf.urls import patterns, include, url

urlpatterns = patterns('senz.views.activity.ActivityMappingView',

    #url(r'^initiate_map/$', 'InitiateMapping'),
    url(r'^mapping/$', 'activity_mapping'),
    url(r'^home_office_status/$', 'home_office_status')
)
