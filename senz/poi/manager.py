# -*- coding: utf-8 -*-
__author__ = 'wuzhifan'

from senz.poi.beacon import Beacon
from senz.common.manager import ManagerBase, MultiThreadManager
from senz.poi.poi import PoiGet

class PoiManager(MultiThreadManager):
    def __init__(self):
        super(PoiManager, self).__init__()

        self.poi_getor = PoiGet()

    def add_poi_to_gps(self, gps):
        poi = self.poi_getor.parse_poi(gps["latitude"], gps["longitude"])
        gps.update(poi)

    def parse_poi(self, context, gps):
        for g in gps:
            self.add_thread(self.add_poi_to_gps, gps=g)
        self.wait()


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

