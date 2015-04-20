# -*- coding:utf-8 -*-
__author__ = 'wuzhifan'

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))

from test_poi import TestPoi
from senz.poi.manager import PoiManager
from senz.activity.UserActivityMapping import UserActivityMapping
from senz.place.LocationRecognition import LocationRecognition

from senz.db.avos.avos_manager import AvosManager
from senz.place.LocationRecognition import LocationRecognition

class TestPoiManager(TestPoi):
    def __init__(self):
        super(TestPoiManager, self).__init__()
        self.manager = PoiManager(pipeline=None, task_name='parse_poi')

    def test_parse_poi(self):
        gps_data = self.get_data()['gps']
        #print gps_data
        context = {}
        print "start parse poi"
        self.manager.parse_poi(context, gps_data)
        count = 0
        for gps in gps_data:
            poi_type = gps.get('poi_type')
            if poi_type:
                count += 1

        if float(count) / float(len(gps_data)) >= 0.9:
            print 'OK'
        else:
            print 'something wrong with poi parse'

class TestActivityManager(object):
    def test_activity_mapping(self):
        activity = {
              "category": "戏剧",
              "foot_print": "bff4679acb3fe7ea5dccdff4fe26ab7f",
              "name": "安徒生经典音乐童话剧《卖火柴的小女孩》\r\n\t    送花0人气+1",
              "source": "DamaiSpider",
              "region": "​小伙伴剧场 - 上海市",
              "ticket": "60",
              "date": {
                "__type": "Date",
                "iso": "2015-06-13T00:00:00.000Z"
              },
              "start_time": {
                "__type": "Date",
                "iso": "2015-06-13T13:30:00.000Z"
              },
              "end_time": {
                "__type": "Date",
                "iso": "2015-06-13T13:30:00.000Z"
              },
              "location": {
                "__type": "GeoPoint",
                "latitude": 31.2279506,
                "longitude": 121.4502026
              },
              "objectId": "55079d0ce4b05a2197d295b2",
              "createdAt": "2015-03-17T11:18:36.552Z",
              "updatedAt": "2015-04-15T21:57:11.760Z"
            }

        user_traces = [{"latitude": 31.2279506,"longitude": 121.4502026, 'timestamp': 1434173400},
                        {"latitude": 31.2279506,"longitude": 121.4502026, 'timestamp': 1434173400},
                        {"latitude": 31.2279506,"longitude": 121.4502026, 'timestamp': 1434173400},
                        {"latitude": 31.2279506,"longitude": 121.4502026, 'timestamp': 1434173400},
                        {"latitude": 31.2279506,"longitude": 121.4502026, 'timestamp': 1434173410},
                        {"latitude": 31.2279506,"longitude": 121.4502026, 'timestamp': 1434173410},
                        {"latitude": 31.2279506,"longitude": 121.4502026, 'timestamp': 1434173410},]

        tool = UserActivityMapping()
        print tool._isInActivity(user_traces, activity)

class TestPlaceManager(object):
    def test_place_recognition(self):
        avos_manager = AvosManager()
        gpslist = avos_manager.getAllData('UserLocation')

        clean_data = []
        for g in gpslist:
            clean_data.append(dict(timestamp = g['timestamp'] / 1000,
                                   latitude=g['location']['latitude'],
                                   longitude=g['location']['longitude']))


        place_recog = LocationRecognition()

        res = place_recog.cluster(clean_data)

        print res[0].__dict__

        return res




if __name__ == '__main__':
    #test_manager = TestPoiManager()
    #test_manager.test_parse_poi()
    #test = TestActivityManager()
    #test.test_activity_mapping()

    manager = TestPlaceManager()
    manager.test_place_recognition()

