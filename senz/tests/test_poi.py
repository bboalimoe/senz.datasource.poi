__author__ = 'wzf'

from base import TestBase



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
            'poi_type' : 'estate',
            'locations' : [{'timestamp': 1427642632501L, 'location': {'latitude': 39.9874398746627, '__type': u'GeoPoint', 'longitude': 116.438323511219053}}]
            }
        print self.testBase(params, 'POST', '/senz/pois/', self.headers)

if __name__ == '__main__':
    test = TestPoi()
    test.testPoiGet()


