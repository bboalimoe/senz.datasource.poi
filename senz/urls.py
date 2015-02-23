from django.conf.urls import patterns, include, url

urlpatterns = patterns('senz.ActivityMappingView',

    url(r'^initial_map/$', 'InitiateMapping'),
    url(r'^get_activity/$', 'GetActivitiesById'),

)

urlpatterns += patterns('senz.TriggerCrawlerView',

    url(r'^trigger_crawler/$', 'TriggerCrawler'),
    url(r'^trigger_crawler_zero/', 'TriggerCrawlerAtZero'),



)

urlpatterns += patterns('senz.PoiTailorView',

    url(r'^$', 'index'),
    url(r'^get_poi/$', 'senz.PoiTailorView.GetPoiByGeoPointAndDev'),
    url(r'^get_poi_groups/$', 'senz.PoiTailorView.GetDevPoiGroups'),

    url(r'^poi_group/$', 'senz.PoiTailorView.PoiGroup'),
    url(r'^poi_group_member/$', 'senz.PoiTailorView.PoiGroupMember'),
    #url(r'^delete_poi_group/$', 'DeletePoiGroup'),
    url(r'^create_poi_group_member/$', 'DeletePoiGroupMember'),
    url(r'^update_poi_group_member/$', 'UpdatePoiGroupMember'),


)

urlpatterns += patterns("senz.GeoFenceView",


    url(r'^create_geofence/$', 'CreateGeoFence'),

                        )


urlpatterns += patterns("senz.BaiduPoiView",


    url(r'^get_baidu_poitype/$', 'GetBaiduPoiType'),

                        )