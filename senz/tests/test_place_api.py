__author__ = 'wzf'

from base import TestBase

class TestPlaceApi(TestBase):
    '''deprecated

    '''
    def __init__(self):
        super(TestPlaceApi, self).__init__()
        self.headers = {"Content-type":"application/json"}
        self.destUserId = "2b4e710aab89f6c5"

    def testLocTag(self):
        url = '/senz/places/user/' + self.destUserId
        method = 'GET'

        self.testBase({}, method, url, self.headers)

    def testAddNearTag(self):
        url = '/senz/places/user/' + self.destUserId + '/tag'
        method = 'GET'

        self.testBase({}, method, url, self.headers)


if __name__ == '__main__':
    testor = TestPlaceApi()
    testor.testLocTag()
    #testor.testAddNearTag()
