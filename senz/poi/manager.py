# -*- coding: utf-8 -*-
__author__ = 'wuzhifan'

import logging

from senz.poi.beacon import Beacon
from senz.common.manager import ManagerBase, MultiThreadManager
from senz.poi.poi import PoiGet
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
    def __init__(self, **kwargs):
        super(PoiManager, self).__init__(**kwargs)
        self.poi_getor = PoiGet()
        self.store_backend = StoreBackend()

    def add_poi_to_gps(self, gps):
        try:
            poi = self.poi_getor.parse_poi(gps["latitude"], gps["longitude"])
            gps.update(poi)
        except Exception, e:

            LOG.error('Error in parse gps point:%s , sys info:%s' % (gps, error_info()))

    def parse_poi(self, context, gps):
        for g in gps:
            self.add_thread(self.add_poi_to_gps, gps=g)
        self.wait()

    def store(self, context):
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


