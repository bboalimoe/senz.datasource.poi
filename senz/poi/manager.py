# -*- coding: utf-8 -*-
__author__ = 'wuzhifan'

from senz.poi.beacon import Beacon
from senz.common.manager import ManagerBase, MultiThreadManager
from senz.poi.poi import PoiGet


def _parseGpsPoi(poiGetor, gps,timestamped_dict, rt):
        #LOG.info('start parse gps %s' % gps)
        results = poiGetor.parsePoi(gps["latitude"], gps["longitude"])
        #LOG.info('parse results %s' % results)

        #print "results", results
        if not results:
            return
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


    def getPoi(self, gpsList, userId):

        GPSlen = len(gpsList)

        GPSrtList = [{} for i in range(GPSlen)]


        usermapping = UserActivityMapping()
        LOG.info('start to store gps list')

        pg = PoiGet()
        #usermapping.dump2db(gpsList,userId)

        timestamped_dict = usermapping.mapActivityByUser(userId)

        self._multiThreadParse(pg, gpsList, timestamped_dict, GPSrtList)

        LOG.info('handle beacon list')

        return {"GPS":GPSrtList}



















    def _coroutineParse(self, poiGetor, gpsList, timestampedDict, rtList):
        #deprecated
        #it should used under 'green' urllib
        i = 0
        for gps in gpsList:
            kwargs = {'poiGetor':poiGetor, 'gps':gps,
                      'timestamped_dict':timestampedDict,
                      'rt':rtList[i]}
            self.threadGroup.add_thread(_parseGpsPoi, poiGetor=poiGetor, gps=gps,
                                                           timestamped_dict=timestampedDict,
                                                           rt=rtList[i])
            i += 1

        self.threadGroup.wait()


    def _singleThreadParse(self, poiGetor, gpsList, timestampedDict, rtList):
        i = 0
        for gps in gpsList:
            _parseGpsPoi(poiGetor, gps, timestampedDict, rtList[i])
            i += 1

    def _multiThreadParse(self, poiGetor, gpsList, timestampedDict, rtList):
        i = 0
        requestArgList = []

        for gps in gpsList:
            kwargs = {'poiGetor':poiGetor, 'gps':gps,
                      'timestamped_dict':timestampedDict,
                      'rt':rtList[i]}
            requestArgList.append(([], kwargs))
            i += 1

        requests = threadpool.makeRequests(_parseGpsPoi, requestArgList)
        [self.threadingPool.putRequest(request) for request in requests]
        self.threadingPool.wait()

    def _handleBeacon(self, beaconList, userId):
        ''' Just dump beacon info to db

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

