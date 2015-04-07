__author__ = 'wzf'

from base import TestBase



class TestPoi(TestBase):
    def __init__(self):
        super(TestBase, self).__init__()
        from senz.common.avos import avos_manager
        self.avos_manager = avos_manager.AvosManager()
        self.headers = {"Content-type":"application/json"}
        self.dest_user_id = "2b4e710aab89f6c5"

    def get_data(self):
        gpsList = self.avos_manager.getAllData('location_record', where='{"userId":"%s"}' % self.dest_user_id)
        return {'gps' : gpsList}

    def testPoiGet(self):
        '''deprecated

        :return:
        '''
        params = {'userId' : self.dest_user_id,
                  'gps' : self.getData()['gps']}
        self.testBase(params, 'POST', '/senz/poi_Gpeacon/')

if __name__ == '__main__':
    test = TestPoi()
    test.testPoiGet()


