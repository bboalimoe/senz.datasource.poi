# -*- coding: utf-8 -*-
__author__ = 'wuzhifan'

import logging

from senz.poi.beacon import Beacon
from senz.common.manager import ManagerBase, MultiThreadManager
from senz.poi.poi import PoiGet

from senz.common.utils import geo_coding, translate

from senz.exceptions import error_info
from senz.db.avos.avos_manager import AvosManager

LOG = logging.getLogger(__name__)

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
        self.poi_getor = geo_coding.GeoCoder(poi_service='tencent')
        self.store_backend = StoreBackend()

    def add_poi_to_gps(self, gps, poi_type=None):
        try:
            if 'location' in gps:
                g = gps['location']
            else:
                g = gps
            pois = self.poi_getor.get_poi(g["latitude"], g["longitude"])
            if poi_type:
                 for i in range(len(pois)-1, -1, -1):
                    #todo: poi type auto increase will be a problem!!
                    #p_type = translate.Trans.poitype_trans(pois[i]['poiType'])
                    if pois[i]['type']['mapping_type'] != poi_type:
                        del pois[i]

            gps['pois'] = pois
        except Exception, e:

            LOG.error('Error in parse gps point:%s , sys info:%s' % (gps, error_info()))

    def parse_poi(self, context, locations, poi_type=None, user_id=None):

        print 'pre parse poi in manager'

        for g in locations:
            self.add_thread(self.add_poi_to_gps, gps=g, poi_type=poi_type)
        self.wait()
        
        print 'poi return locations : %s' % locations

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



