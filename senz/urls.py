from django.conf.urls import patterns, include, url

urlpatterns = patterns('senz.views.activity.ActivityMappingView',

    url(r'^initiate_map/$', 'InitiateMapping'),
    url(r'^activity/$', 'GetActivitiesById'),

)

'''
urlpatterns += patterns('senz.TriggerCrawlerView',

    url(r'^trigger_crawler/$', 'TriggerCrawler'),
    url(r'^trigger_crawler_zero/', 'TriggerCrawlerAtZero'),

)
'''


urlpatterns += patterns('senz.views.poi.PoiTailorView',

    url(r'^$', 'index'),
    url(r'^poi/$', 'GetPoiByGeoPointAndDev'),
    url(r'^poi_groups/$', 'GetDevPoiGroups'),

    url(r'^poi_group/$', 'PoiGroup'),
    url(r'^poi_group_member/$', 'PoiGroupMember'),



)


urlpatterns += patterns("senz.views.poi.GeoFenceView",


    url(r'^create_geofence/$', 'CreateGeoFence'),

                        )


urlpatterns += patterns("senz.views.poi.BaiduPoiView",


    url(r'^baidu_poitype/$', 'GetBaiduPoiType'),

                        )


urlpatterns += patterns("senz.views.location.LocationRecoView",

    url(r'^usr_loc_tag/$', 'GetUserLocationTags'),

                        )


urlpatterns += patterns("senz.views.poi.PoiView",

    url(r'^poi_Gpeacon/$', 'GetPoi'),

                        )