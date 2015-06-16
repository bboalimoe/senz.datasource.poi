from django.conf.urls import patterns, include, url

from SenzPoi.senz.views.poi.urls import urlpatterns as poi_urls
from SenzPoi.senz.views.activity.urls import urlpatterns as activity_urls
from SenzPoi.senz.views.place.urls import urlpatterns as place_urls

urlpatterns = patterns('',
    url(r'^pois/', include(poi_urls)),
    url(r'^activities/', include(activity_urls)),
    url(r'^places/', include(place_urls)),
)




