# -*- coding:utf-8 -*-
__author__ = 'wzf'

import logging

from senz.poi.poi import PoiGet
from senz.activity.UserActivityMapping import UserActivityMapping
from senz.poi.beacon import Beacon

from senz.common.openstack.threadgroup import ThreadGroup

from senz.exceptions import *

LOG = logging.getLogger(__name__)

class PoiController(object):
    def __init__(self):
        self.threadGroup = ThreadGroup()

    def _parseGpsPoi(self, poiGetor, gps,timestamped_dict, rt):
        results = poiGetor.parsePoi(gps["latitude"], gps["longitude"])

        print "results", results
        poiType, poiName = results['poiType'], results['name']
        rt.setdefault("poiType",poiType)
        rt.setdefault("locDescription",poiName)  #poiname => locDescription
        timestamp_ = gps['timestamp']
        rt.setdefault("timestamp", timestamp_)


        if timestamp_ in timestamped_dict.keys():
            rt.setdefault("actiType",timestamped_dict[str(timestamp_)]["category"])
            rt.setdefault("actiName",timestamped_dict[str(timestamp_)]["name"])

            rt.setdefault("actiDescription",timestamped_dict[str(timestamp_)]["region"])
            rt.setdefault("actiStartTime",timestamped_dict[str(timestamp_)]["start_time"])
            rt.setdefault("actiEndTime",timestamped_dict[str(timestamp_)]["end_time"])


    def _handleBeacon(self, beaconList, userId):

        if beaconList:
            beacon = Beacon()
            beacon.dump2db(beaconList,userId)

            Beaconlen = len(beaconList)
            BeaconrtList = [{} for i in range(Beaconlen)]

            return beacon.BeaconInfo(BeaconrtList)
        else:
            return []



    def getPoi(self, beaconList, gpsList, userId):

        GPSlen = len(gpsList)
        rtBeaLoc = {"GPS":" ","iBeacon":" "}


        #todo 1.每来一次请求就把数据存入后端 2.beacon和gps数据存完后，调用匹配算法算制定userid匹配出的活动


        GPSrtList = [{} for i in range(GPSlen)]



        usermapping = UserActivityMapping()
        LOG.info('start to store gps list')
        pg = PoiGet()
        usermapping.dump2db(gpsList,userId)

        LOG.info('mapping user activity')
        timestamped_dict = usermapping.mapActivityByUser(userId)

        #todo
        #gps poitype
        i = 0
        LOG.info('parse poi')
        for gps in gpsList:
            self.threadGroup.add_thread(self._parseGpsPoi, poiGetor=pg, gps=gps,
                                                           timestamped_dict=timestamped_dict,
                                                           rt=GPSrtList[i])
            i += 1

        #beacon poitype
        LOG.info('handle beacon list')
        BeaconrtList = self._handleBeacon(beaconList, userId)

        return rtBeaLoc.update({"GPS":GPSrtList,"iBeacon":BeaconrtList})