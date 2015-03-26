# -*- coding:utf-8 -*-
__author__ = 'wzf'

import logging

from webob import exc

from senz.poi.poi import PoiGet
from senz.activity.UserActivityMapping import UserActivityMapping
from senz.poi.beacon import Beacon

LOG = logging.getLogger(__name__)

class PoiController(object):
    def getPoi(self, beaconList, gpsList, userId):
        Beaconlen = len(beaconList)
        GPSlen = len(gpsList)
        rtBeaLoc = {"GPS":" ","iBeacon":" "}


        #todo 1.每来一次请求就把数据存入后端 2.beacon和gps数据存完后，调用匹配算法算制定userid匹配出的活动
        try:

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


                results = pg.parsePoi(gps["latitude"], gps["longitude"])
                print "results", results
                poiType, poiName = results['poiType'], results['name']
                GPSrtList[i].setdefault("poiType",poiType)
                GPSrtList[i].setdefault("locDescription",poiName)  #poiname => locDescription
                timestamp_ = gps['timestamp']
                GPSrtList[i].setdefault("timestamp", timestamp_)


                if timestamp_ in timestamped_dict.keys():
                    GPSrtList[i].setdefault("actiType",timestamped_dict[str(timestamp_)]["category"])
                    GPSrtList[i].setdefault("actiName",timestamped_dict[str(timestamp_)]["name"])

                    GPSrtList[i].setdefault("actiDescription",timestamped_dict[str(timestamp_)]["region"])
                    GPSrtList[i].setdefault("actiStartTime",timestamped_dict[str(timestamp_)]["start_time"])
                    GPSrtList[i].setdefault("actiEndTime",timestamped_dict[str(timestamp_)]["end_time"])
                i += 1
            #beacon poitype

            BeaconrtList = beacon.BeaconInfo(BeaconrtList)



        except Exception, e:
            LOG.error('Error in get poi: %s' % e)
            return exc.HTTPInternalServerError()
            pass



        return rtBeaLoc.update({"GPS":GPSrtList,"iBeacon":BeaconrtList})


if __name__ == '__main__':
    print exc.HTTPInternalServerError()
