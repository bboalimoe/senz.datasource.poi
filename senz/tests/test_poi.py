__author__ = 'wzf'

from base import TestBase
import json


class TestPoi(TestBase):
    def __init__(self):
        super(TestBase, self).__init__()
        self.headers = {"Content-type":"application/json"}
        self.dest_user_id = "2b4e710aab89f6c5"

    def get_data(self):
        gpsList = self.avos_manager.getAllData('location_record', where='{"userId":"%s"}' % self.dest_user_id)
        return {'gps' : gpsList}

    def testPoiGet(self):
        params = {
            #'poi_type' : 'estate',
            'locations' : [{'timestamp': 1427642632501L, 'location': {'latitude': 39.96957, '__type': u'GeoPoint', 'longitude': 116.391648}}]
            }
        res = self.testBase(params, 'POST', '/senz/pois/', self.headers)
        dic = json.loads(res)
        print json.dumps(dic, encoding='UTF-8', ensure_ascii=False)
        #print res.encode('utf-8')

if __name__ == '__main__':
    test = TestPoi()
    test.testPoiGet()


