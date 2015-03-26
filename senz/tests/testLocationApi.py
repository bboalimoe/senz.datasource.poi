__author__ = 'wzf'

from base import TestBase

class TestLocationApi(TestBase):
    def __init__(self):

        self.headers = {"Content-type":"application/json"}
        self.destUserId = "2b4e710aab89f6c5"

    def testLocTag(self):
        params = {"userId": self.destUserId,}

        self.testBase(params, "POST", "/senz/usr_loc_tag/")

    def testAddNearTag(self):
        params = {"userId": self.destUserId,}

        self.testBase(params, "POST", "/senz/add_near_tag/")


if __name__ == '__main__':
    testor = TestLocationApi()
    #testor.testLocTag()
    testor.testAddNearTag()

