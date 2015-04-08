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

{"results": [{"status": "", "ratio": 0.9242718446601942, "objectId": "5524df9de4b087afeb152802", "estimateTime": 11020000, "userId": "2b4e710aab89f6c5", "longitude": 116.34389969678843, "latitude": 39.8972862516112, "tag": "home", "updatedAt": "2015-04-08T07:58:21.859Z", "date": "", "createdAt": "2015-04-08T07:58:21.859Z"},
             {"status": "", "ratio": 0.9544303797468354, "objectId": "5524df9de4b087afeb152803", "estimateTime": 11020000, "userId": "2b4e710aab89f6c5", "longitude": 116.34389969678843, "latitude": 39.8972862516112, "tag": "office", "updatedAt": "2015-04-08T07:58:21.902Z", "date": "", "createdAt": "2015-04-08T07:58:21.902Z"}]}

{"results": "[{\"latitude\": 39.8972862516112, \"estimateTime\": 11020000, \"longitude\": 116.34389969678843, \"tags\": [{\"estimateTime\": 4760000, \"tag\": \"home\", \"ratio\": 0.9242718446601942}, {\"estimateTime\": 3770000, \"tag\": \"office\", \"ratio\": 0.9544303797468354}]}]"}
