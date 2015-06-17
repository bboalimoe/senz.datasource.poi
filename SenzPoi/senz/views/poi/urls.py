from django.conf.urls import patterns, include, url

poi_groups_patterns = patterns('senz.views.poi.PoiGroupView',
    #url(r'^$', 'index'),
    url(r'^$',  'GetDevPoiGroups'),
    url(r'^(?P<id>[A-Za-z0-9\-]+)/$', 'PoiGroup'),

    #url(r'^poi/$', 'GetPoiByGeoPointAndDev'),     combined with r'^$'
    url(r'^member/$', 'PoiGroupMember'),
)

urlpatterns = patterns('',
    url(r'^$', 'senz.views.poi.PoiView.parse_poi'),
    url(r'^groups/$', include(poi_groups_patterns)),
)



