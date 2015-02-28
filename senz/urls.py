from django.conf.urls import patterns, include, url

urlpatterns = patterns('senz.ActivityMappingView',

    url(r'^initiate_map/$', 'InitiateMapping'),
    url(r'^activity/$', 'GetActivitiesById'),

)

urlpatterns += patterns('senz.TriggerCrawlerView',

    url(r'^trigger_crawler/$', 'TriggerCrawler'),
    url(r'^trigger_crawler_zero/', 'TriggerCrawlerAtZero'),



)


urlpatterns += patterns('senz.PoiTailorView',

    url(r'^$', 'index'),
    url(r'^poi/$', 'senz.PoiTailorView.GetPoiByGeoPointAndDev'),
    url(r'^poi_groups/$', 'senz.PoiTailorView.GetDevPoiGroups'),

    url(r'^poi_group/$', 'senz.PoiTailorView.PoiGroup'),
    url(r'^poi_group_member/$', 'senz.PoiTailorView.PoiGroupMember'),



)


urlpatterns += patterns("senz.GeoFenceView",


    url(r'^create_geofence/$', 'CreateGeoFence'),

                        )


urlpatterns += patterns("senz.BaiduPoiView",


    url(r'^baidu_poitype/$', 'GetBaiduPoiType'),

                        )


urlpatterns += patterns("senz.LocationRecoView",

    url(r'^usr_loc_tag/$', 'GetUserLocationTags'),

                        )