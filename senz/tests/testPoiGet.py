__author__ = 'wzf'

from base import TestBase

from senz.common.avos import avos_manager

class TestPoiGet(TestBase):
    def __init__(self):
        self.avosManager = avos_manager.AvosManager()
        self.headers = {"Content-type":"application/json"}
        self.destUserId = "2b4e710aab89f6c5"

    def getData(self):
        gpsList = self.avosManager.getAllData('location_record', where='{"userId":"%s"}' % self.destUserId)
        return {'GPS' : gpsList}

    def testPoiGet(self):
        params = {'userId' : self.destUserId,
                  'GPS' : self.getData()['GPS']}
        self.testBase(params, 'POST', '/senz/poi_Gpeacon/')

if __name__ == '__main__':
    test = TestPoiGet()
    test.testPoiGet()


