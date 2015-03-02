# -*- encoding=utf-8 -*-
__author__ = 'zhanghengyang'



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

        self.beaconRtList = {}

    def dump2db(self,beaconlist,userId):
        """
        dump the info to db
        :return:
        """

        for beacon in beaconlist:
            result = self.avosManager.saveData("UserBeaconTrace",{"major":beacon['major'],"minor":beacon["minor"],"uuid":beacon["uuid"],"activityId":"",
                                                           "timpstamp":beacon['timestamp'],"userId":userId})
            if not result:
               print "save error: userid:%s".format(userId)

    def BeaconInfo(self,beaconlist):


        for beacon,i in beaconlist,range(len(beaconlist)):


            self.beaconRtList[i].setdefault("poiType","")
            self.beaconRtList[i].setdefault("timestamp","")
            self.beaconRtList[i].setdefault("locDescription","")


            self.beaconRtList[i].setdefault("actiType","")
            self.beaconRtList[i].setdefault("actiName","")

            self.beaconRtList[i].setdefault("actiDescription","")
            self.beaconRtList[i].setdefault("actiStartTime","")
            self.beaconRtList[i].setdefault("actiEndTime","")


        return self.beaconRtList