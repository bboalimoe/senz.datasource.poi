# -*- coding:utf-8 -*-
__author__ = 'wuzhifan'

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))

from senz.tests.test_poi import TestPoi
from senz.poi.manager import PoiManager
from senz.activity.UserActivityMapping import UserActivityMapping

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
              "category": "音乐",
              "foot_print": "8a12b9396649d8b66c920cd18ee8421d",
              "name": "BIGBANG—2015 WORLD TOUR [MADE] IN GUANGZHOU",
              "source": "DoubanSpider",
              "region": "广州 萝岗区 广州国际体育演艺中心",
              "ticket": "费用：\n580元 / 880元 / 1280元 / 1480元 / 1680元",
              "date": {
                "__type": "Date",
                "iso": "2015-05-30T00:00:00.000Z"
              },
              "ACL": {
                "*": {
                  "write": True,
                  "read": True
                }
              },
              "start_time": {
                "__type": "Date",
                "iso": "2015-05-30T19:30:00.000Z"
              },
              "end_time": {
                "__type": "Date",
                "iso": "2015-05-31T21:30:00.000Z"
              },
              "location": {
                "__type": "GeoPoint",
                "latitude": 23.175709,
                "longitude": 113.482376
              },
              "objectId": "556054afe4b00c57d9a52620",
              "createdAt": "2015-05-23T18:21:35.095Z",
              "updatedAt": "2015-05-23T18:21:35.095Z"
            }
        user_traces = [{"latitude": 23.175709,"longitude": 113.482376, 'timestamp': 1432985400000},
                       {"latitude": 23.175709,"longitude": 113.482376, 'timestamp': 1432985410000},
                       {"latitude": 23.175709,"longitude": 113.482376, 'timestamp': 1432985420000},
                       {"latitude": 23.175709,"longitude": 113.482376, 'timestamp': 1432985430000},
                       {"latitude": 23.175709,"longitude": 113.482376, 'timestamp': 1432985440000},
                       {"latitude": 23.175709,"longitude": 113.482376, 'timestamp': 1432985450000},
                       {"latitude": 23.175709,"longitude": 113.482376, 'timestamp': 1432985460000},
                       {"latitude": 23.175709,"longitude": 113.482376, 'timestamp': 1432985470000},
                       {"latitude": 23.175709,"longitude": 113.482376, 'timestamp': 1432985480000},
                       {"latitude": 23.175709,"longitude": 113.482376, 'timestamp': 1432985490000},]

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
    test = TestActivityManager()
    test.test_activity_mapping()

    #manager = TestPlaceManager()
    #manager.test_place_recognition()

