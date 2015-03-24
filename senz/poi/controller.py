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


    def getPoi(self, beaconList, gpsList, userId):
        Beaconlen = len(beaconList)
        GPSlen = len(gpsList)
        rtBeaLoc = {"GPS":" ","iBeacon":" "}


        #todo 1.每来一次请求就把数据存入后端 2.beacon和gps数据存完后，调用匹配算法算制定userid匹配出的活动


        GPSrtList = [{} for i in range(GPSlen)]

        BeaconrtList = [{} for i in range(Beaconlen)]

        usermapping = UserActivityMapping()
        beacon = Beacon()
        pg = PoiGet()
        usermapping.dump2db(gpsList,userId)
        beacon.dump2db(beaconList,userId)

        timestamped_dict = usermapping.mapActivityByUser(userId)

        #todo
        #gps poitype
        i = 0
        for gps in gpsList:
            self.threadGroup.add_thread(self._parseGpsPoi, poiGetor=pg, gps=gps,
                                                           timestamped_dict=timestamped_dict,
                                                           rt=GPSrtList[i])
            i += 1

        #beacon poitype

        BeaconrtList = beacon.BeaconInfo(BeaconrtList)

        return rtBeaLoc.update({"GPS":GPSrtList,"iBeacon":BeaconrtList})