__author__ = 'wzf'

import httplib
import json


class TestLocationApi(object):
    def __init__(self):
        self.host = "127.0.0.1:8088"
        self.headers = {"Content-type":"application/json"}
        self.conn = httplib.HTTPConnection(self.host)
        self.destUserId = "2b4e710aab89f6c5"

    def testBase(self, params, method, url):
        self.conn.request(method, url,
                          json.JSONEncoder().encode(params),
                          self.headers)

        print "json.JSONEncoder().encode(params)   ", \
                              json.JSONEncoder().encode(params)


        respon = self.conn.getresponse()
        data = respon.read()
        print data

        self.conn.close()

    def testLocTag(self):
        params = {"userId": self.destUserId,}

        self.testBase(params, "POST", "/senz/usr_loc_tag/")

    def testAddNearTag(self):
        params = {"userId": self.destUserId,}

        self.testBase(params, "POST", "/senz/add_near_tag/")


if __name__ == '__main__':
    testor = TestLocationApi()
    testor.testLocTag()
    #testor.testAddNearTag()

