# -*- encoding=utf-8 -*-
__author__ = 'zhanghengyang'

import sys

sys.path.append("../utils")
from senz.common.avos.avos_manager import *


#todo including the ibeacon poitype

#firstly return the mocking data

class Beacon(object):

    """
    "iBeacon": [{

    "poiType": POI_TYPE,
    "timestamp": timestamp,
    "locDescription": DESCRIPTION, （地点位置描述）
    "actiTpye": ACTI_TYPE,（活动类型，无则没有这项）
    "actiDescription": ACTI_DESCRIPTION,（活动描述，无则没有这项）
    "actiStartTime": ACTI_START_TIME（活动开始时间，无则没有这项）
    "actiEndTime": ACTI_END_TIME（活动结束时间，无则没有这项）
    }, ...]



    ####NOTICE
    #####ME
    #####HA
    ibeacon can't return the activity like gps by algo
    it should be the admin who update the activity info correspoding to the beacon
    """
    def __init__(self):

        self.beaconRtList = []
        self.avosManager = AvosManager()

    def dump2db(self,beaconlist,userId):
        """
        dump the info to db
        :return:
        """
        avosClassName = "UserBeaconTrace"
        i = 0
        for i in range(0, len(beaconlist), 200):
            j = i + 200 if i + 200 > len(beaconlist) else len(beaconlist)
            locationtList = []
            for k in range(i ,j):
                beacon = beaconlist[k]
                locationtList.append({ "latitude":beacon['latitude'],"longitude":beacon["longitude"],
                                      "activityId":"", "timestamp":beacon['timestamp'],"near":"",
                                      "userId":userId})

            self.avosManager.saveData(avosClassName, locationtList)



    def BeaconInfo(self,beaconlist):

        i = 0
        self.beaconRtList = [{} for bea in beaconlist]
        for beacon in beaconlist:


            self.beaconRtList[i].setdefault("poiType","")
            self.beaconRtList[i].setdefault("timestamp","")
            self.beaconRtList[i].setdefault("locDescription","")


            self.beaconRtList[i].setdefault("actiType","")
            self.beaconRtList[i].setdefault("actiName","")

            self.beaconRtList[i].setdefault("actiDescription","")
            self.beaconRtList[i].setdefault("actiStartTime","")
            self.beaconRtList[i].setdefault("actiEndTime","")
            i += 1

        return self.beaconRtList