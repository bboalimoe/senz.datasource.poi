# -*- coding: utf-8 -*-
from senz.common.utils import geo_coding, geoutils

__author__ = 'wuzhifan'

import logging
import json

from senz.poi.beacon import Beacon
from senz.common.manager import ManagerBase, MultiThreadManager
from senz.common.utils import geo_coding, geoutils
from senz.db.avos.avos_manager import AvosManager

from geopy.distance import vincenty

LOG = logging.getLogger(__name__)
DEFAULT_SAME_LOCATION_THRESHOLD = 0.03 #km

class StoreBackend(object):
    '''Simple store backend use leancloud
    '''
    def __init__(self):
        self.avos_class = 'UserLocationTrace'
        self.avos_manager = AvosManager()

    def store(self, data):
        self.avos_manager.saveData(self.avos_class, data)


class PoiManager(MultiThreadManager):
    def __init__(self, *args, **kwargs):
        super(PoiManager, self).__init__(*args, **kwargs)
        self.tecent_poi_getor = geo_coding.GeoCoder(poi_service='tencent')
        self.baidu_poi_getor = geo_coding.GeoCoder(poi_service='baidu')
        self.store_backend = StoreBackend()
        self.avos_manager = AvosManager()

    def _mix_pois(self, t1, t2):
        res_pois = []
        for p1 in t1:
            for p2 in t2:
                dist = geoutils.distance(p1['location']['latitude'], p1['location']['longitude'],
                                      p2['location']['latitude'], p2['location']['longitude'])



                if dist < DEFAULT_SAME_LOCATION_THRESHOLD \
                        and p1['type']['mapping_type'] == p2['type']['mapping_type']:
                    # assume these are same poi
                    res_pois.append(p1)
                else:
                    res_pois.append(p1)
                    res_pois.append(p2)


        return res_pois


    def add_poi_to_gps(self, gps, userId, poi_type=None):

        if 'location' in gps:
            g = gps['location']
        else:
            g = gps
        tecent_pois = self.tecent_poi_getor.get_poi(g["latitude"], g["longitude"])
        #baidu_pois = self.baidu_poi_getor.get_poi(g["latitude"], g["longitude"])

        #pois = self._mix_pois(tecent_pois, baidu_pois)
        pois = tecent_pois
        if poi_type:
             for i in range(len(pois)-1, -1, -1):
                #todo: poi type auto increase will be a problem!!
                #p_type = translate.Trans.poitype_trans(pois[i]['poiType'])
                if pois[i]['type']['mapping_type'] != poi_type:
                    del pois[i]

        homeoffice = self.get_home_office(gps, userId)

        gps['pois'] = pois
        gps['user_place'] = homeoffice


    def get_home_office(self, gps, userId):
        homeoffice = []
        user_pointer = {"__type": "Pointer", "className": '_User', "objectId": userId}
        userPlaces = self.avos_manager.getAllData('place', where='{"user":%s}' % json.dumps(user_pointer))

        closeToHome = 0.15 #kilometers
        gpsLoc = gps['location']
        gpsGeo = (gpsLoc['latitude'], gpsLoc['longitude'])
        for place in userPlaces:
            avLoc = place['location']
            placeGeo = (avLoc['latitude'], avLoc['longitude'])
            distance = vincenty(placeGeo, gpsGeo).kilometers

            if distance < closeToHome:
                homeoffice.append(place)

        return homeoffice


    def parse_poi(self, context, locations, userId, poi_type=None):

        print 'pre parse poi in manager'

        for g in locations:
            self.add_thread(self.add_poi_to_gps, gps=g, userId=userId, poi_type=poi_type)
        self.wait()
        
        #print 'poi return locations : %s' % locations

        return locations

    def store(self, context):
        ''' deprecated

        '''
        if self.task_name in context['results']:
            res = context['results'][self.task_name]
            self.store_backend.store(res)

    def _handleBeacon(self, beaconList, userId):
        ''' Just dump beacon info to db.

        Beacon functions are almost not involved now, this may be deprecated

        :param beaconList:
        :param userId:
        :return:
        '''

        if beaconList:
            beacon = Beacon()
            beacon.dump2db(beaconList,userId)

            Beaconlen = len(beaconList)
            BeaconrtList = [{} for i in range(Beaconlen)]

            return beacon.BeaconInfo(BeaconrtList)
        else:
            return []


class PoiGroupManager(ManagerBase):
    pass



