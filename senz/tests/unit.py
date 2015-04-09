__author__ = 'wuzhifan'

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))

from test_poi import TestPoi
from senz.poi.manager import PoiManager

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

if __name__ == '__main__':
    test_manager = TestPoiManager()
    test_manager.test_parse_poi()

